from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .poll import Poll  # noqa: F401
    from .user import User  # noqa: F401


class Vote(Base):
    __table_args__ = (
        UniqueConstraint('poll_id', 'voter_id', name='uix_vote_poll_voter'),
    )

    id = Column(Integer, primary_key=True, index=True)
    date_vote = Column(DateTime, index=True, nullable=False)
    weight = Column(Float, nullable=False)
    voter_id = Column(String, nullable=False)
    poll_id = Column(String, ForeignKey("poll.id"))
    poll = relationship("Poll", back_populates="votes")
