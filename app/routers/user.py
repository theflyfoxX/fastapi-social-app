from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.services.user_service import UserService
from app.schemas.user import UserOut, UserCreate
from app.config.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user.
    """
    return UserService.create_user(user, db)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves a user by ID.
    """
    return UserService.get_user(user_id, db)
