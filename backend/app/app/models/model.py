from typing import TYPE_CHECKING

from sqlalchemy import JSON, TIMESTAMP, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .product import Product  # noqa: F401


class Model(Base):
    id = Column(String, primary_key=True, index=True)
    last_updated = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )
    name = Column(String, index=True)
    tournament = Column(Integer)
    nmr_staked = Column(Numeric)
    latest_ranks = Column(JSON)
    latest_reps = Column(JSON)
    latest_returns = Column(JSON)
    round_model_performances = Column(JSON)
    start_date = Column(TIMESTAMP)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="models")
    products = relationship("Product", back_populates="model")
