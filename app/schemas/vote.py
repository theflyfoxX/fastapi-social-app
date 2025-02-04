from pydantic import BaseModel, conint
from uuid import UUID

class VoteBase(BaseModel):
    post_id: UUID
    dir: conint(le=1)  # type: ignore
