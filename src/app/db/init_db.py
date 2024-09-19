import asyncio
import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy.engine import Engine

from app.api.deps import get_async_session, get_user_db
from app.db import base  # noqa: F401
from app.schemas import UserCreate
from app.user_manager import get_user_manager

# make sure all SQL Alchemy models are imported (app.db.base)
# before initializing DB otherwise, SQL Alchemy might fail to
# initialize relationships properly for more details:
# https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28




get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=is_superuser
                        )
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")


def init_db() -> None:
    asyncio.run(create_user("admin@gmail.com", "admin_password", is_superuser=True))
