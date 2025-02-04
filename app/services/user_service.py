from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password

class UserService:
    @staticmethod
    def create_user(user_data: UserCreate, db: Session):
        """
        Creates a new user.
        """
        hashed_password = hash_password(user_data.password)
        user_data_dict = user_data.model_dump()
        user_data_dict["password"] = hashed_password

        new_user = User(**user_data_dict)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user(user_id: UUID, db: Session):
        """
        Retrieves a user by ID.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} does not exist"
            )
        return user
