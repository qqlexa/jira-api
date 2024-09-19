from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Task, TaskAssignee, User
from app.mail_service import MailService
from app.schemas import TaskCreate, TaskInDB, TaskUpdate, UserRead


async def validate_assignees(db: AsyncSession, assignees: list[str]):
    for assignee in assignees:
        user_result = await db.execute(select(User).filter_by(id=assignee))
        user = user_result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Assignee user ID {assignee} does not exist.",
            )


async def _create_task(db: AsyncSession, task: TaskCreate, user_id: UUID) -> Task:
    task_dict = task.dict()
    assignees = [str(assignee) for assignee in task_dict.pop("assignees")]
    await validate_assignees(db, assignees)

    try:
        params = {**task_dict, "responsible_user_id": str(user_id)}
        db_task = Task(**params)
        db.add(db_task)
        await db.flush()
        for assignee in assignees:
            db_task_assignee = TaskAssignee(task_id=db_task.id, user_id=assignee)
            db.add(db_task_assignee)

        await db.commit()
        await db.refresh(db_task)
        return db_task
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while creating the task.",
        )


async def _get_task(db: AsyncSession, task_id: int) -> Task:
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def _get_tasks(db: AsyncSession) -> list[Task]:
    result = await db.execute(select(Task))
    return result.scalars().all()


async def _update_task(
    db: AsyncSession, task_id: int, task_update: TaskUpdate, mail_service: MailService
) -> Task:
    try:
        task = await _get_task(db, task_id)
        previous_status = task.status
        for key, value in task_update.dict(exclude_unset=True).items():
            setattr(task, key, value)

        if task.status != previous_status:
            responsible_user_id = str(task.responsible_user_id)
            mail_service.send_mail(
                recipients=[responsible_user_id],
                subject=f"Update status in Task{task_id}",
                body=f"Status updated to {task.status}",
            )

        await db.commit()
        await db.refresh(task)
        return task
    except IntegrityError as e:
        await db.rollback()
        if "responsible_user_id" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Responsible user ID does not exist.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while updating the task.",
        )


async def _delete_task(db: AsyncSession, task_id: int) -> None:
    task = await _get_task(db, task_id)
    await db.delete(task)
    await db.commit()
