from typing import Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import BaseModel

from app.enums import PriorityEnum, RoleEnum, StatusEnum


class UserRead(schemas.BaseUser[str]):
    id: str
    first_name: str | None = None
    last_name: str | None = None
    role: RoleEnum

    @classmethod
    def model_validate(cls, data):
        # Override the default validation process
        if isinstance(data.id, UUID):
            # Convert UUID to string if necessary
            data.id = str(data.id)

        # Call the default Pydantic validation
        return super().model_validate(data)


class UserCreate(schemas.BaseUserCreate):
    first_name: str | None = None
    last_name: str | None = None
    role: RoleEnum


class UserUpdate(schemas.BaseUserCreate):
    first_name: str | None = None
    last_name: str | None = None
    role: RoleEnum


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    responsible_user_id: UUID
    status: StatusEnum = StatusEnum.TODO
    priority: PriorityEnum = PriorityEnum.MEDIUM


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.TODO
    priority: PriorityEnum = PriorityEnum.MEDIUM
    assignees: list[UUID]


class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum
    priority: PriorityEnum


class TaskInDB(TaskBase):
    id: int

    class Config:
        orm_mode = True
