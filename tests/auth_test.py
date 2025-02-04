import pytest
import logging
from unittest.mock import MagicMock
from app.services.auth_service import AuthService
from app.schemas.auth import TokenData
from jose import jwt
from fastapi import HTTPException, status
from uuid import uuid4
from app.utils.security import hash_password

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Mock settings for testing
from app.config.settings import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

# ✅ Setup Mock Database Session
@pytest.fixture
def mock_db():
    return MagicMock()

# ✅ Test Token Creation
def test_create_access_token():
    user_id = uuid4()
    token = AuthService.create_access_token(user_id)
    
    assert isinstance(token, str)
    
    # ✅ Decode the token and check the payload
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["id"] == str(user_id)
    assert "exp" in decoded

# ✅ Test Token Verification (Valid Token)
def test_verify_access_token():
    user_id = uuid4()
    token = AuthService.create_access_token(user_id)
    
    token_data = AuthService.verify_access_token(token, HTTPException(status_code=401))
    assert isinstance(token_data, TokenData)
    assert token_data.id == str(user_id)

# ✅ Test Token Verification (Invalid Token)
def test_verify_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        AuthService.verify_access_token("invalid.token.here", HTTPException(status_code=401))
    
    assert exc_info.value.status_code == 401

# ✅ Test Login (Valid Credentials)
def test_login_valid_user(mock_db):
    user_mock = MagicMock()
    user_mock.id = uuid4()
    user_mock.email = "saad@gmail.com"
    user_mock.password = hash_password("saad")

    mock_db.query().filter().first.return_value = user_mock

    class MockOAuth2PasswordRequestForm:
        username = "saad@gmail.com"
        password = "saad"

    form_data = MockOAuth2PasswordRequestForm()

    token = AuthService.login(form_data, mock_db)

    assert token.access_token is not None
    assert token.token_type == "bearer"
    assert token.id == str(user_mock.id)

# ✅ Test Login (Invalid Password)
def test_login_invalid_password(mock_db):
    user_mock = MagicMock()
    user_mock.id = uuid4()
    user_mock.email = "saad@gmail.com"
    user_mock.password = hash_password("saad")

    mock_db.query().filter().first.return_value = user_mock

    class MockOAuth2PasswordRequestForm:
        username = "saad@gmail.com"
        password = "saad123"

    form_data = MockOAuth2PasswordRequestForm()

    with pytest.raises(HTTPException) as exc_info:
        AuthService.login(form_data, mock_db)

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Invalid Credentials"

# ✅ Test Login (User Not Found)
def test_login_user_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    class MockOAuth2PasswordRequestForm:
        username = "nonexistent@example.com"
        password = "password"

    form_data = MockOAuth2PasswordRequestForm()

    with pytest.raises(HTTPException) as exc_info:
        AuthService.login(form_data, mock_db)

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Invalid Credentials"
