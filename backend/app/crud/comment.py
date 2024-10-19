import logging
from datetime import date, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import case, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.models.comment import Comment
from backend.app.models.post import Post
from backend.app.schemas.comment import CommentAnalytics, CommentCreate, CommentUpdate
from backend.app.schemas.user import UserRead
from backend.app.utils.general import moderate_content
from backend.app.utils.tasks import generate_auto_response

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

    post = await db.get(Post, comment.post_id)
    if post and post.auto_reply:
        logger.info("Creating task for auto AI response")
        generate_auto_response.apply_async(
            args=[db_comment.id, post.id], countdown=post.reply_delay
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


async def get_comments_daily_breakdown(
    db: AsyncSession, date_from: date, date_to: date
) -> list[CommentAnalytics]:
    result = await db.execute(
        select(
            func.date(Comment.created_at).label("date"),
            func.count(Comment.id).label("total_comments"),
            func.sum(case((Comment.is_blocked, 1), else_=0)).label("blocked_comments"),
        )
        .filter(
            Comment.created_at >= date_from,
            Comment.created_at <= date_to + timedelta(days=1),
        )
        .group_by(func.date(Comment.created_at))
        .order_by(func.date(Comment.created_at))
    )
    return [
        CommentAnalytics(
            date=row._mapping["date"].isoformat(),
            total_comments=row._mapping["total_comments"],
            blocked_comments=row._mapping["blocked_comments"],
        )
        for row in result.all()
    ]
