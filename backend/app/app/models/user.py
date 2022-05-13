""" Database model for user """

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .favorite import Favorite  # noqa: F401
    from .product import Product  # noqa: F401
    from .model import Model  # noqa: F401
    from .order import Order  # noqa: F401
    from .poll import Poll  # noqa: F401
    from .review import Review  # noqa: F401
    from .vote import Vote  # noqa: F401
    from .coupon import Coupon  # noqa: F401


class User(Base):
    """Database model for user"""

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
    numerai_api_key_can_upload_submission = Column(Boolean, nullable=True)
    numerai_api_key_can_stake = Column(Boolean, nullable=True)
    numerai_api_key_can_read_submission_info = Column(Boolean, nullable=True)
    numerai_api_key_can_read_user_info = Column(Boolean, nullable=True)
    date_last_numerai_sync = Column(DateTime)
    numerai_wallet_address = Column(String, nullable=True, unique=True)
    public_key = Column(String)
    encrypted_private_key = Column(String)
    social_rocketchat = Column(String, nullable=True)
    social_linkedin = Column(String, nullable=True)
    social_twitter = Column(String, nullable=True)
    social_website = Column(String, nullable=True)
    products = relationship("Product", back_populates="owner")
    models = relationship("Model", back_populates="owner")
    orders = relationship("Order", back_populates="buyer")
    reviews = relationship("Review", back_populates="reviewer")
    favorites = relationship("Favorite", back_populates="user")
    polls = relationship("Poll", back_populates="owner")
    coupons = relationship(
        "Coupon", foreign_keys="Coupon.owner_id", back_populates="owner"
    )
    created_coupons = relationship(
        "Coupon", foreign_keys="Coupon.creator_id", back_populates="creator"
    )
