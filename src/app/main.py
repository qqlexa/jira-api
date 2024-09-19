import uvicorn
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import Authenticator
from fastapi_users.authentication.strategy import JWTStrategy
from fastapi_users.router import get_auth_router, get_register_router

from app.api import auth
from app.api.endpoints import api_router
from app.config import settings

# Create the FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/api/docs",
)

# Include your existing API router
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(auth.router)


# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )  # pragma: no cover
