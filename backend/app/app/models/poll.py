from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .vote import Vote  # noqa: F401


class Poll(Base):
    id = Column(String, primary_key=True, index=True)
    date_creation = Column(DateTime, index=True, nullable=False)
    date_finish = Column(DateTime, index=True, nullable=False)
    topic = Column(String, index=True)
    description = Column(String, index=True)
    options = Column(ARRAY(JSON))
    is_multiple = Column(Boolean, default=False)
    max_options = Column(Integer, default=1)
    is_anonymous = Column(Boolean, default=True)
    is_blind = Column(Boolean, default=True)
    is_numerai_only = Column(Boolean, default=True)
    is_stake_predetermined = Column(Boolean, default=True)
    weight_mode = Column(String, default="stake")
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="polls")
    votes = relationship("Vote", back_populates="poll")