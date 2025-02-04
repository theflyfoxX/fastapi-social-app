from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.vote_service import VoteService
from app.schemas.vote import VoteBase
from app.oauth2 import get_current_user
from uuid import UUID

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote_data: VoteBase,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Adds or removes a vote for a post.
    """
    return VoteService.vote(vote_data, db, current_user.id)
