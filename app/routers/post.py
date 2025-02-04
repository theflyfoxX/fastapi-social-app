from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.services.post_service import PostService
from app.schemas.post import PostOut, PostCreate, PostUpdate, PostWithVotes
from app.config.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/{post_id}", response_model=PostWithVotes)
def get_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieves a single post.
    """
    return PostService.get_post(post_id, db)

@router.get("/", response_model=List[PostWithVotes])
def get_posts(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = 10, 
    skip: int = 0, 
    search: Optional[str] = ""
):
    """
    Retrieves all posts.
    """
    return PostService.get_posts(db, limit, skip, search)

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """
    Creates a new post.
    """
    return PostService.create_post(post, db, current_user.id)

@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: UUID,  
    updated_post: PostUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """
    Updates a post.
    """
    return PostService.update_post(post_id, updated_post, db, current_user.id)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: UUID,  
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """
    Deletes a post.
    """
    PostService.delete_post(post_id, db, current_user.id)
    return {"message": "Post deleted successfully"}

