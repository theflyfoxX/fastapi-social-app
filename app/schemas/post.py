from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.schemas.user import UserOut

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostOut(PostBase):
    id: UUID
    created_at: datetime
    owner_id: UUID
    owner: UserOut

    class Config:
        from_attributes = True

class PostWithVotes(BaseModel):
    post: PostOut
    votes: int

    class Config:
        from_attributes = True
