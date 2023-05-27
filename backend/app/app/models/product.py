""" Database model for product """

from typing import TYPE_CHECKING

from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .favorite import Favorite  # noqa: F401
    from .user import User  # noqa: F401
    from .category import Category  # noqa: F401
    from .model import Model  # noqa: F401
    from .artifact import Artifact  # noqa: F401
    from .product_option import ProductOption  # noqa: F401
    from .review import Review  # noqa: F401


class Product(Base):
    """Database model for product"""

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    sku = Column(String, index=True, nullable=False, unique=True)
    avatar = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, server_default="t")
    use_encryption = Column(Boolean, server_default="f")
    is_ready = Column(Boolean)
    is_daily = Column(Boolean, server_default="f")
    expiration_round = Column(Integer)
    total_qty_sales = Column(Integer, default=0, server_default="0")
    total_qty_sales_filtered = Column(Integer, default=0, server_default="0")
    total_qty_delivered = Column(Integer, default=0, server_default="0")
    total_num_sales = Column(Integer, default=0, server_default="0")
    last_sale_price = Column(Numeric)
    last_sale_price_delta = Column(Numeric)
    webhook = Column(String)
    featured_products = Column(ARRAY(Integer))
    round_lock = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="products")
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", lazy="subquery")
    model_id = Column(String, ForeignKey("model.id"))
    model = relationship("Model", lazy="select", back_populates="products")
    artifacts = relationship("Artifact", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    favorites = relationship(
        "Favorite", back_populates="product", cascade="all, delete-orphan"
    )
    options = relationship(
        "ProductOption", back_populates="product", cascade="all, delete-orphan"
    )
