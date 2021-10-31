from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .product import Product  # noqa: F401


class Favorite(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    user = relationship("User", back_populates="favorites")
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="favorites", lazy="subquery")
