from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import current_active_user
from app.api.deps import get_async_session, get_mail_service
from app.db.models import Task, TaskAssignee, User
from app.enums import RoleEnum
from app.mail_service import MailService
from app.schemas import TaskCreate, TaskInDB, TaskUpdate, UserRead
from app.services import (
    _create_task,
    _get_task,
    _get_tasks,
    _update_task,
    _delete_task,
)


api_router = APIRouter(dependencies=[Depends(current_active_user)])


async def check_manager_role(user: User = Depends(current_active_user)) -> User:
    if user.role != RoleEnum.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return user


@api_router.post("/tasks/", response_model=TaskInDB)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(check_manager_role),
):
    return await _create_task(db, task, user.id)


@api_router.get("/tasks/{task_id}", response_model=TaskInDB)
async def read_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    return await _get_task(db, task_id)


@api_router.get("/tasks/", response_model=list[TaskInDB])
async def read_tasks(db: AsyncSession = Depends(get_async_session)):
    return await _get_tasks(db)


@api_router.put("/tasks/{task_id}", response_model=TaskInDB)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
    mail_service: MailService = Depends(get_mail_service),
):
    return await _update_task(db, task_id, task_update, mail_service)


@api_router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(
    task_id: int, db: AsyncSession = Depends(get_async_session), user: User = Depends(check_manager_role)
):
    await _delete_task(db, task_id)
    return {"ok": True}
