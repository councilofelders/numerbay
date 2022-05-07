""" Database model for order artifact """

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .order import Order  # noqa: F401


class OrderArtifact(Base):
    """Database model for order artifact"""

    __tablename__ = "order_artifact"  # type: ignore
    id = Column(String, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    round_tournament = Column(Integer, index=True)
    description = Column(String)
    url = Column(String)
    object_name = Column(String, index=True, nullable=True)
    object_size = Column(Integer, nullable=True)
    state = Column(String, nullable=False, default="pending", server_default="pending")
    is_numerai_direct = Column(Boolean, nullable=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    order = relationship("Order", back_populates="artifacts")
