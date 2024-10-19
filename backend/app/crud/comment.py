import logging
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.models.comment import Comment
from backend.app.schemas.comment import CommentCreate, CommentUpdate
from backend.app.schemas.user import UserRead
from backend.app.utils.general import moderate_content

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_comment(
    db: AsyncSession, comment: CommentCreate, user: UserRead
) -> Comment:
    is_blocked = not await moderate_content(comment.content)
    db_comment = Comment(**comment.model_dump(), user_id=user.id, is_blocked=is_blocked)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)

    if is_blocked:
        logger.warning("Inappropriate content detected for user: %s", user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment contains inappropriate content",
        )

    return db_comment


async def get_comments(db: AsyncSession) -> list[Comment]:
    return (await db.execute(select(Comment))).scalars().all()


async def get_comment(db: AsyncSession, comment_id: str) -> Comment:
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    comment = result.scalars().first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comment


async def update_comment(
    db: AsyncSession, comment_id: str, comment_update: CommentUpdate
) -> Comment:
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalars().first()

    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    for key, value in comment_update.model_dump().items():
        if value is not None:
            setattr(db_comment, key, value)

    db_comment.updated_at = datetime.utcnow()
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def delete_comment(db: AsyncSession, comment_id: str) -> Comment:
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalars().first()

    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    db_comment.is_deleted = True
    db_comment.updated_at = datetime.utcnow()
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment
