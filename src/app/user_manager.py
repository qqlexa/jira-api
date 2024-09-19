# app/managers/user_manager.py
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session

from app.api.deps import get_async_session, get_user_db
from app.config import settings
from app.db.models import User


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def validate_password(self, password: str, user: User) -> None:
        if len(password) < 8:
            raise exceptions.InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        # Add more password validation rules here if needed

    async def on_after_register(self, user: User, request: Optional[object] = None):
        print(f"User {user.id} has registered.")


# Dependency to get the UserManager
async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
