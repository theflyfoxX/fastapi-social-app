from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.models.vote import Vote
from sqlalchemy import func

class PostService:
    @staticmethod
    def create_post(post: PostCreate, db: Session, current_user_id: UUID):
        """
        Creates a new post.
        """
        new_post = Post(owner_id=current_user_id, **post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    @staticmethod
    def update_post(post_id: UUID, updated_post: PostUpdate, db: Session, current_user_id: UUID):
        """
        Updates a post if the user is the owner.
        """
        post_query = db.query(Post).filter(Post.id == post_id)
        post = post_query.first()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} does not exist"
            )

        if post.owner_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post"
            )

        post_query.update(updated_post.model_dump(), synchronize_session=False)
        db.commit()
        return post_query.first()

    @staticmethod
    def delete_post(post_id: UUID, db: Session, current_user_id: UUID):
        """
        Deletes a post if the user is the owner.
        """
        post_query = db.query(Post).filter(Post.id == post_id)
        post = post_query.first()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} does not exist"
            )

        if post.owner_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post"
            )

        post_query.delete(synchronize_session=False)
        db.commit()

    @staticmethod
    def get_post(post_id: UUID, db: Session):
        """
        Retrieves a single post.
        """
        post = db.query(Post, func.count(Vote.post_id).label("votes")) \
                .join(Vote, Vote.post_id == Post.id, isouter=True) \
                .group_by(Post.id) \
                .filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found"
            )
        
        return {"post": post[0], "votes": post[1]}

    @staticmethod
    def get_posts(db: Session, limit: int, skip: int, search: str):
        """
        Retrieves multiple posts.
        """
        posts = db.query(Post, func.count(Vote.post_id).label("votes")) \
                .join(Vote, Vote.post_id == Post.id, isouter=True) \
                .group_by(Post.id) \
                .filter(Post.title.contains(search)) \
                .limit(limit).offset(skip).all()

        return [{"post": post[0], "votes": post[1]} for post in posts]
