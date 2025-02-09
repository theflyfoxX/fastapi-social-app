import pytest
import logging
from unittest.mock import MagicMock
from app.services.vote_service import VoteService
from app.schemas.vote import VoteBase
from app.models.vote import Vote
from uuid import uuid4
from fastapi import HTTPException, status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_db():
    return MagicMock()

def test_vote_post_not_found(mock_db):
    vote_data = VoteBase(post_id=uuid4(), dir=1)
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        VoteService.vote(vote_data, mock_db, uuid4())

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

def test_vote_already_voted(mock_db):
    vote_data = VoteBase(post_id=uuid4(), dir=1)
    user_id = uuid4()
    vote_mock = MagicMock()

    mock_db.query().filter().first.return_value = vote_mock

    with pytest.raises(HTTPException) as exc_info:
        VoteService.vote(vote_data, mock_db, user_id)

    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    
# add tests for all cases
