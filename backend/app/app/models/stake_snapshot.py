""" Database model for stake snapshot """

from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .model import Model  # noqa: F401


class StakeSnapshot(Base):
    __table_args__ = (
        UniqueConstraint(
            "round_tournament",
            "name",
            "tournament",
            name="uix_stake_snapshot_round_name_tournament",
        ),
    )

    __tablename__ = "stake_snapshot"  # type: ignore
    id = Column(Integer, primary_key=True, index=True)
    date_creation = Column(DateTime, index=True, nullable=False)
    round_tournament = Column(
        Integer, index=True, nullable=False, default=293, server_default="293"
    )
    name = Column(String, index=True, nullable=False)
    tournament = Column(Integer, index=True, nullable=False)
    nmr_staked = Column(Numeric, nullable=True)
    return_13_weeks = Column(Numeric, nullable=True)
    return_52_weeks = Column(Numeric, nullable=True)
    payout_pending = Column(Numeric, nullable=True)
    model_id = Column(String, ForeignKey("model.id", ondelete="CASCADE"))
    model = relationship("Model", back_populates="snapshot")
