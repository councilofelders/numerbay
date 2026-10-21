""" Database model for user """

from typing import TYPE_CHECKING, Optional

from cryptography.fernet import InvalidToken
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.core import crypto
from app.core.config import settings
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
    pending_email = Column(String, nullable=True)
    email_verified = Column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    token_version = Column(Integer, nullable=False, default=0, server_default="0")
    numerai_api_key_public_id = Column(String, nullable=True)
    numerai_api_key_secret_stored = Column(
        "numerai_api_key_secret", String, nullable=True
    )  # holds ciphertext after backfill; plaintext during transition
    numerai_api_key_secret_backup = Column(
        String, nullable=True
    )  # plaintext mirror, dropped after cutover

    @property
    def numerai_api_key_secret(self) -> Optional[str]:
        """Effective Numerai API secret"""
        stored = self.numerai_api_key_secret_stored
        if stored is None:
            return None
        if stored.startswith("gAAA"):
            try:
                return crypto.decrypt_secret(stored)
            except InvalidToken:
                backup = self.numerai_api_key_secret_backup
                if backup is not None:
                    print(f"WARN: decrypt failed for user {self.id}, " "using backup")
                    return backup
                raise
        return stored  # plaintext during transition

    @numerai_api_key_secret.setter
    def numerai_api_key_secret(self, value: Optional[str]) -> None:
        if value and settings.DATA_ENCRYPTION_KEY:
            self.numerai_api_key_secret_stored = crypto.encrypt_secret(value)
        else:
            self.numerai_api_key_secret_stored = value
        self.numerai_api_key_secret_backup = value

    numerai_api_key_can_upload_submission = Column(Boolean, nullable=True)
    numerai_api_key_can_stake = Column(Boolean, nullable=True)
    numerai_api_key_can_read_submission_info = Column(Boolean, nullable=True)
    numerai_api_key_can_read_user_info = Column(Boolean, nullable=True)
    date_last_numerai_sync = Column(DateTime)
    numerai_wallet_address = Column(String, nullable=True, unique=True)
    default_receiving_wallet_address = Column(String, nullable=True, unique=True)
    public_key = Column(String)
    encrypted_private_key = Column(String)
    public_key_v2 = Column(String)
    encrypted_private_key_v2 = Column(String)
    social_rocketchat = Column(String, nullable=True)
    social_discord = Column(String, nullable=True)
    social_linkedin = Column(String, nullable=True)
    social_twitter = Column(String, nullable=True)
    social_website = Column(String, nullable=True)
    props = Column(JSON, nullable=True)
    date_registered = Column(DateTime, nullable=True, server_default=func.now())
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
