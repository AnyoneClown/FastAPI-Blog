from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import CurrentActiveUser, get_async_session
from backend.app.crud.comment import (
    create_comment,
    delete_comment,
    get_comment,
    get_comments,
    update_comment,
)
from backend.app.schemas.comment import CommentCreate, CommentInDB, CommentUpdate
from backend.app.schemas.user import UserRead

router = APIRouter()


@router.post("/", response_model=CommentInDB)
async def create_comment_route(
    comment: CommentCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRead = Depends(CurrentActiveUser),
):
    return await create_comment(db=db, comment=comment, user=current_user)


@router.get("/", response_model=List[CommentInDB])
async def get_comments_route(db: AsyncSession = Depends(get_async_session)):
    return await get_comments(db=db)


@router.get("/{comment_id}/", response_model=CommentInDB)
async def get_comment_route(
    comment_id: str, db: AsyncSession = Depends(get_async_session)
):
    return await get_comment(db=db, comment_id=comment_id)


@router.put("/{comment_id}/", response_model=CommentInDB)
async def update_comment_route(
    comment_id: str,
    comment_update: CommentUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRead = Depends(CurrentActiveUser),
):
    return await update_comment(
        db=db, comment_id=comment_id, comment_update=comment_update
    )


@router.delete("/{comment_id}/", response_model=CommentInDB)
async def delete_comment_route(
    comment_id: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRead = Depends(CurrentActiveUser),
):
    return await delete_comment(db=db, comment_id=comment_id)
