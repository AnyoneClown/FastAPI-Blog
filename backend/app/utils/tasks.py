import asyncio
import logging
from uuid import UUID

from sqlalchemy.future import select

from backend.app.api.deps import async_session_maker, celery_app
from backend.app.core.config import settings
from backend.app.models.comment import Comment
from backend.app.models.post import Post
from backend.app.models.user import User
from backend.app.utils.general import generate_response

logger = logging.getLogger(__name__)


@celery_app.task
def generate_auto_response(comment_id: UUID, post_id: UUID):
    asyncio.run(_generate_auto_response(comment_id, post_id))


async def _generate_auto_response(comment_id: UUID, post_id: UUID):
    logger.info(
        "Starting auto-response generation for post ID: %s and comment ID: %s",
        post_id,
        comment_id,
    )

    async with async_session_maker() as db:
        try:
            query = select(User).where(User.email == "ai_user@example.com")
            result = await db.execute(query)
            ai_user = result.scalars().first()

            if not ai_user:
                logger.info("AI user not found, creating new AI user.")
                ai_user = User(
                    email="ai_user@example.com",
                    hashed_password=settings.AI_USER_PASSWORD,
                    is_active=True,
                    is_superuser=True,
                )
                db.add(ai_user)
                await db.commit()
                await db.refresh(ai_user)

            post = await db.get(Post, post_id)
            comment = await db.get(Comment, comment_id)

            ai_response = await generate_response(
                post_title=post.title,
                post_content=post.content,
                comment_content=comment.content,
            )

            db_comment = Comment(
                content=ai_response, post_id=post.id, user_id=ai_user.id
            )
            db.add(db_comment)
            await db.commit()
            await db.refresh(db_comment)

        except Exception as e:
            logger.error("Error in auto-response generation: %s", str(e))
            raise
