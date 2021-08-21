from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401
    from .product import Product  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    public_address = Column(String, index=True, nullable=True, unique=True)
    nonce = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    numerai_api_key_public_id = Column(String, nullable=True)
    numerai_api_key_secret = Column(String, nullable=True)
    items = relationship("Item", back_populates="owner")
    products = relationship("Product", back_populates="owner")
    orders = relationship("Order", back_populates="buyer")
