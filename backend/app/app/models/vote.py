from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .poll import Poll  # noqa: F401
    from .user import User  # noqa: F401


class Vote(Base):
    __table_args__ = (
        UniqueConstraint('poll_id', 'voter_id', 'option', name='uix_vote_poll_voter_option'),
    )

    id = Column(Integer, primary_key=True, index=True)
    date_vote = Column(DateTime, index=True, nullable=False)
    option = Column(Integer, index=True, nullable=False)
    weight_basis = Column(Numeric)
    final_weight = Column(Numeric)
    voter_id = Column(String, index=True, nullable=False)
    voter_address = Column(String)
    poll_id = Column(String, ForeignKey("poll.id", ondelete="CASCADE"))
    poll = relationship("Poll", back_populates="votes")
