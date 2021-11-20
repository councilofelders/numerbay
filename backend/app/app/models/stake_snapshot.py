from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, JSON, Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .model import Model  # noqa: F401


class StakeSnapshot(Base):
    __tablename__ = "stake_snapshot"  # type: ignore
    id = Column(Integer, primary_key=True, index=True)
    date_creation = Column(DateTime, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    tournament = Column(Integer, index=True, nullable=False)
    nmr_staked = Column(Numeric, nullable=True)
    return_13_weeks = Column(Numeric, nullable=True)
    return_52_weeks = Column(Numeric, nullable=True)
    payout_pending = Column(Numeric, nullable=True)
    model_id = Column(String, ForeignKey("model.id", ondelete="CASCADE"))
    model = relationship("Model", back_populates="snapshot")
