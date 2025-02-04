import pytest
import logging
from unittest.mock import MagicMock
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.models.user import User
from app.utils.hashing import hash_password
from fastapi import HTTPException, status
from uuid import uuid4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_db():
    return MagicMock()

def test_create_user(mock_db):
    user_data = UserCreate(email="elonmusk@gmail.com", password="tesla123")
    user_mock = MagicMock()
    user_mock.id = uuid4()
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = user_mock

    new_user = UserService.create_user(user_data, mock_db)

    assert new_user is not None

def test_get_existing_user(mock_db):
    user_mock = MagicMock()
    user_mock.id = uuid4()
    user_mock.email = "saad@gmail.com"

    mock_db.query().filter().first.return_value = user_mock

    user = UserService.get_user(user_mock.id, mock_db)
    assert user.id == user_mock.id

def test_get_user_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        UserService.get_user(uuid4(), mock_db)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
