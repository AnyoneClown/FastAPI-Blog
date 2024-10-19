import datetime
import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.models.base import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(String)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=None, nullable=True)
    is_blocked = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
