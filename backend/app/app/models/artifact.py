""" Database model for artifact """

from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .product import Product  # noqa: F401


class Artifact(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    round_tournament = Column(Integer, index=True)
    description = Column(String)
    url = Column(String)
    object_name = Column(String, index=True, nullable=True)
    object_size = Column(Integer, nullable=True)
    state = Column(String, nullable=False, default="pending", server_default="pending")
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="artifacts")
