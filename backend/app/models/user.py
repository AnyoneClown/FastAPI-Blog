from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship

from backend.app.models.base import Base
from backend.app.models.comment import Comment


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    posts = relationship("Post", back_populates="author")
    comments = relationship(Comment, back_populates="author")
