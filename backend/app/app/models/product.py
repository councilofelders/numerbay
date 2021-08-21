from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .category import Category
    from .model import Model


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    sku = Column(String, index=True, nullable=False, unique=True)
    is_on_platform = Column(Boolean, nullable=False, default=True, server_default='f')
    price = Column(Numeric, index=True, nullable=False)
    currency = Column(String, nullable=False, default="USD", server_default="USD")
    chain = Column(String)
    avatar = Column(String)
    third_party_url = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="products")
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", lazy="subquery")
    model_id = Column(String, ForeignKey("model.id"))
    model = relationship("Model", lazy='subquery', back_populates="products")
