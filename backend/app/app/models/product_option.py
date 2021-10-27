from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .product import Product  # noqa: F401


class ProductOption(Base):
    __tablename__ = "product_option"  # type: ignore
    id = Column(Integer, primary_key=True, index=True)
    is_on_platform = Column(Boolean, nullable=False, default=True, server_default="f")
    third_party_url = Column(String)
    description = Column(String)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric, index=True, nullable=False)
    currency = Column(String, nullable=False, default="USD", server_default="USD")
    wallet = Column(String, nullable=True)
    chain = Column(String)
    stake_limit = Column(Numeric, nullable=True)
    mode = Column(String, nullable=True)
    is_active = Column(Boolean, server_default="t")
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="options")
