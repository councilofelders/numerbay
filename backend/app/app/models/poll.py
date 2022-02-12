""" Database model for poll """

from typing import TYPE_CHECKING

from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .vote import Vote  # noqa: F401


class Poll(Base):
    """ Database model for poll """

    id = Column(String, primary_key=True, index=True)
    date_creation = Column(DateTime, index=True, nullable=False)
    date_finish = Column(DateTime, index=True, nullable=False)
    topic = Column(String, index=True)
    description = Column(String, index=True)
    options = Column(ARRAY(JSON))
    is_finished = Column(Boolean, default=False)
    is_multiple = Column(Boolean, default=False)
    max_options = Column(Integer, default=1)
    is_anonymous = Column(Boolean, default=True)
    is_blind = Column(Boolean, default=True)
    stake_basis_round = Column(Integer)
    weight_mode = Column(String, default="equal")
    is_stake_predetermined = Column(Boolean, default=True)
    min_stake = Column(Numeric, nullable=True)
    min_rounds = Column(Integer, nullable=True)
    clip_low = Column(Numeric, nullable=True)
    clip_high = Column(Numeric, nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="polls")
    votes = relationship("Vote", back_populates="poll", cascade="all, delete-orphan")
