from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.session import SessionLocal
from app.mail_service import JiraFakeMailService, MailService


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_mail_service() -> MailService:
    mail_service = JiraFakeMailService()
    try:
        yield mail_service
    finally:
        pass
