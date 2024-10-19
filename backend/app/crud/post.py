import logging
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.models.post import Post
from backend.app.schemas.post import PostCreate, PostUpdate
from backend.app.schemas.user import UserRead
from backend.app.utils.general import moderate_content

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_post(db: AsyncSession, post: PostCreate, user: UserRead) -> Post:
    is_blocked = not await moderate_content(post.content)
    db_post = Post(**post.model_dump(), user_id=user.id, is_blocked=is_blocked)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)

    if is_blocked:
        logger.warning("Inappropriate content detected for user: %s", user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post contains inappropriate content",
        )

    return db_post


async def get_posts(db: AsyncSession) -> list[Post]:
    return (await db.execute(select(Post))).scalars().all()


async def get_post(db: AsyncSession, post_id: str) -> Post:
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


async def delete_post(db: AsyncSession, post_id: str) -> Post:
    result = await db.execute(select(Post).filter(Post.id == post_id))
    db_post = result.scalars().first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    db_post.is_deleted = True
    db_post.updated_at = datetime.utcnow()
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def update_post(db: AsyncSession, post_id: str, post_update: PostUpdate) -> Post:
    result = await db.execute(select(Post).filter(Post.id == post_id))
    db_post = result.scalars().first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    for key, value in post_update.model_dump().items():
        if value is not None:
            setattr(db_post, key, value)

    db_post.updated_at = datetime.utcnow()
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post
