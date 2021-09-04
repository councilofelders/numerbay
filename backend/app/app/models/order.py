from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .product import Product  # noqa: F401


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    date_order = Column(DateTime, index=True, nullable=False)
    round_order = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    chain = Column(String, nullable=False, default="ethereum")
    from_address = Column(String)
    to_address = Column(String)
    transaction_hash = Column(String)
    state = Column(String)
    buyer_id = Column(Integer, ForeignKey("user.id"))
    buyer = relationship("User", back_populates="orders")
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", lazy="subquery")
