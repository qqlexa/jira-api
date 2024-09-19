from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.enums import PriorityEnum, RoleEnum, StatusEnum


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.DEVELOPER)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    responsible_user_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.TODO)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.MEDIUM)

    assignees = relationship("User", secondary="task_assignees")


class TaskAssignee(Base):
    __tablename__ = "task_assignees"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    user_id = Column(GUID, ForeignKey("users.id"), primary_key=True)
