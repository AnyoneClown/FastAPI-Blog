from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    auto_reply: bool = Field(default=False)
    reply_delay: int = Field(default=0, ge=0)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostInDB(PostBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    is_blocked: bool
    is_deleted: bool

    class Config:
        from_attributes = True
