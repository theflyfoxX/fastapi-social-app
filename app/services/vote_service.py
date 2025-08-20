from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.vote import Vote
from app.models.post import Post
from app.schemas.vote import VoteBase

class VoteService:
    @staticmethod
    def vote(vote_data: VoteBase, db: Session, user_id: UUID):
        """
        Handles upvoting and removing votes from a post.
        """
        post = db.query(Post).filter(Post.id == vote_data.post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {vote_data.post_id} does not exist"
            )

        vote_query = db.query(Vote).filter(
            Vote.post_id == vote_data.post_id, Vote.user_id == str(user_id)  
        )
        sample_query = vote_query.all()
        found_vote = vote_query.first()
        if vote_data.dir == 1:
            if found_vote:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User {user_id} has already voted on post {vote_data.post_id}"
                )
            new_vote = Vote(post_id=vote_data.post_id, user_id=str(user_id)) 
            db.add(new_vote)
            db.commit()
            return {"message": "Successfully added vote"}
        else:
            if not found_vote:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vote does not exist"
                )
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Successfully deleted vote"}
