from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .product import Product  # noqa: F401
    from .user import User  # noqa: F401


class Review(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, index=True, nullable=False)
    round_tournament = Column(Integer, index=True)
    rating = Column(Integer, index=True, nullable=False)
    text = Column(String)
    is_verified_order = Column(Boolean)
    reviewer_id = Column(Integer, ForeignKey("user.id"))
    reviewer = relationship("User", back_populates="reviews")
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="reviews")
