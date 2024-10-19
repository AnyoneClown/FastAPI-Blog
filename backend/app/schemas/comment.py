from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    post_id: UUID


class CommentUpdate(BaseModel):
    content: str | None = None


class CommentInDB(CommentBase):
    id: UUID
    post_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    is_blocked: bool
    is_deleted: bool

    class Config:
        orm_mode = True


class CommentAnalytics(BaseModel):
    date: str
    total_comments: int
    blocked_comments: int
