from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import CurrentActiveUser, get_async_session
from backend.app.crud.post import (
    create_post,
    delete_post,
    get_post,
    get_posts,
    update_post,
)
from backend.app.schemas.post import PostCreate, PostInDB, PostUpdate
from backend.app.schemas.user import UserRead

router = APIRouter()


@router.post("/", response_model=PostInDB)
async def create_post_route(
    post: PostCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRead = Depends(CurrentActiveUser),
):
    return await create_post(db=db, post=post, user=current_user)


@router.get("/", response_model=List[PostInDB])
async def get_posts_route(db: AsyncSession = Depends(get_async_session)):
    return await get_posts(db=db)


@router.get("/{post_id}/", response_model=PostInDB)
async def get_post_router(post_id: str, db: AsyncSession = Depends(get_async_session)):
    return await get_post(db=db, post_id=post_id)


@router.put("/{post_id}/", response_model=PostInDB)
async def update_post_route(
    post_id: str,
    post_update: PostUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRead = Depends(CurrentActiveUser),
):
    return await update_post(db=db, post_id=post_id, post_update=post_update)


@router.delete("/{post_id}/", response_model=PostInDB)
async def delete_post_route(
    post_id: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRead = Depends(CurrentActiveUser),
):
    return await delete_post(db=db, post_id=post_id)
