from jose import JWTError, jwt
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.config.settings import settings
from app.schemas.auth import Token, TokenData
from app.models.user import User
from app.config.database import get_db
from app.utils.security import verify_password


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class AuthService:
    """
    Authentication service for handling login and token creation.
    """

    @staticmethod
    def create_access_token(user_id: UUID) -> str:
        """
        Generate JWT access token.
        """
        to_encode = {"id": str(user_id)}
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_access_token(token: str, credentials_exception) -> TokenData:
        """
        Verify and decode JWT token.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("id")

            if user_id is None:
                raise credentials_exception

            return TokenData(id=user_id)
        except JWTError:
            raise credentials_exception

    @staticmethod
    def login(user_credentials: OAuth2PasswordRequestForm, db: Session = Depends(get_db)) -> Token:
        """
        Authenticate user and return JWT token.
        """
        user = db.query(User).filter(User.email == user_credentials.username).first()

        if not user or not verify_password(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Credentials"
            )

        access_token = AuthService.create_access_token(user_id=user.id)

        return Token(
            access_token=access_token,
            token_type="bearer",
            id=str(user.id)
        )
