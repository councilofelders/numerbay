""" Database model for coupon """

from typing import TYPE_CHECKING

from sqlalchemy import (
    ARRAY,
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
    from .order import Order  # noqa: F401
    from .user import User  # noqa: F401


class Coupon(Base):
    """Database model for coupon"""

    id = Column(Integer, primary_key=True, index=True)
    date_creation = Column(DateTime, index=True, nullable=False)
    date_expiration = Column(DateTime, index=True)
    code = Column(String, index=True, nullable=False)
    applicability = Column(String, index=True, nullable=False)
    applicable_product_ids = Column(ARRAY(Integer))
    applicable_seller_id = Column(Integer)
    min_spend = Column(Numeric)
    max_discount = Column(Numeric)
    discount_mode = Column(String, nullable=False)
    discount_percent = Column(Integer)
    state = Column(String, index=True)
    quantity_total = Column(Integer, index=True)
    is_owned_by_seller = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", foreign_keys=owner_id, back_populates="coupons")
    creator_id = Column(Integer, ForeignKey("user.id"))
    creator = relationship("User", foreign_keys=creator_id, back_populates="created_coupons")
    redemptions = relationship(
        "Order", back_populates="applied_coupon", cascade="all, delete-orphan"
    )
