import pytest
import logging
from unittest.mock import MagicMock
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate
from app.models.post import Post
from uuid import uuid4
from fastapi import HTTPException, status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_db():
    return MagicMock()

def test_create_post(mock_db):
    post_data = PostCreate(title="What a great day in Maimi!", content="Best day ever!!")
    current_user_id = uuid4()
    post_mock = MagicMock()
    post_mock.id = uuid4()

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = post_mock

    new_post = PostService.create_post(post_data, mock_db, current_user_id)
    assert new_post is not None

def test_update_post_not_found(mock_db):
    post_id = uuid4()
    post_data = PostUpdate(title="What a bad day!!", content="Updated Content to a Bad day!")

    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        PostService.update_post(post_id, post_data, mock_db, uuid4())

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
