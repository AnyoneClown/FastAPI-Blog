import uvicorn
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.app.api.deps import CurrentActiveUser, auth_backend, fastapi_users
from backend.app.api.routes.comments import router as comments_router
from backend.app.api.routes.post import router as posts_router
from backend.app.core.config import settings
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserRead, UserUpdate

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])


@app.get("/")
async def root_handler():
    return {"Hello": "World!"}


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(CurrentActiveUser)):
    return {"message": f"Hello {user.email}!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="info")
