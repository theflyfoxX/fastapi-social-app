from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

    def as_dict(self):
        """Convert object to dictionary for JSON serialization."""
        return {
            "user_id": str(self.user_id),
            "post_id": str(self.post_id)
        }
