from typing import TYPE_CHECKING

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .coupon import Coupon  # noqa: F401
    from .user import User  # noqa: F401
    from .product import Product  # noqa: F401
    from .order_artifact import OrderArtifact  # noqa: F401


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    date_order = Column(DateTime, index=True, nullable=False)
    round_order = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=1, server_default="1")
    price = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    mode = Column(String, nullable=False, default="file", server_default="file")
    stake_limit = Column(Numeric, nullable=True)
    submit_model_id = Column(String, nullable=True)
    submit_model_name = Column(String, nullable=True)
    submit_state = Column(String)
    last_submit_round = Column(Integer)
    chain = Column(String, nullable=False, default="ethereum")
    from_address = Column(String)
    to_address = Column(String)
    transaction_hash = Column(String, index=True, unique=True)
    coupon = Column(Boolean)
    coupon_specs = Column(JSON)
    state = Column(String)
    buyer_public_key = Column(String)
    buyer_id = Column(Integer, ForeignKey("user.id"))
    buyer = relationship("User", back_populates="orders")
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", lazy="subquery")
    applied_coupon_id = Column(Integer, ForeignKey("coupon.id", ondelete="CASCADE"))
    applied_coupon = relationship("Coupon", back_populates="redemptions")
    artifacts = relationship("OrderArtifact", back_populates="order")
