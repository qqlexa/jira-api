from fastapi import APIRouter, Request
from fastapi.security import HTTPBearer
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)

from app.config import settings
from app.db.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.user_manager import get_user_manager


class HTTPBearerTokenOnly(HTTPBearer):
    async def __call__(self, request: Request) -> str | None:  # type: ignore
        credentials = await super().__call__(request)
        if credentials:
            return credentials.credentials
        return None


class SimpleBearerTransport(BearerTransport):
    def __init__(self):  # noqa
        self.scheme = HTTPBearerTokenOnly()  # type: ignore


bearer_transport = SimpleBearerTransport()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, str](
    get_user_manager=get_user_manager,  # Define this function based on FastAPI users documentation
    auth_backends=[auth_backend],
)

current_active_user = fastapi_users.current_user()

router = APIRouter()

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
