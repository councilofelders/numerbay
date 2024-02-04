""" Data schema for user """

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas import Coupon

# Shared properties
from .model import ModelMinimal


class UserBase(BaseModel):
    """Base data schema for user"""

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    username: Optional[str] = None
    public_address: Optional[str] = None
    default_receiving_wallet_address: Optional[str] = None
    date_last_numerai_sync: Optional[datetime] = None
    social_discord: Optional[str] = None
    social_linkedin: Optional[str] = None
    social_twitter: Optional[str] = None
    social_website: Optional[str] = None
    props: Optional[dict] = None


# Properties to receive via API on creation
class UserCreate(BaseModel):
    """Create data schema for user"""

    username: str
    password: str
    email: Optional[EmailStr] = None
    public_address: Optional[str] = None
    signature: Optional[str] = None
    nonce: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on update
class UserUpdate(UserBase):  # pylint: disable=too-many-instance-attributes
    """Update data schema for user"""

    password: Optional[str] = None
    signature: Optional[str] = None
    nonce: Optional[str] = None
    numerai_api_key_public_id: Optional[str] = None
    numerai_api_key_secret: Optional[str] = None
    public_key: Optional[str] = None
    encrypted_private_key: Optional[str] = None
    public_key_v2: Optional[str] = None
    encrypted_private_key_v2: Optional[str] = None
    factor: Optional[float] = None


class UserInDBBase(UserBase):
    """Base database data schema for user"""

    id: Optional[int] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    """API data schema for user"""

    numerai_api_key_public_id: Optional[str] = None
    numerai_api_key_can_upload_submission: Optional[bool] = None
    numerai_api_key_can_stake: Optional[bool] = None
    numerai_api_key_can_read_submission_info: Optional[bool] = None
    numerai_api_key_can_read_user_info: Optional[bool] = None
    numerai_wallet_address: Optional[str] = None
    public_key: Optional[str] = None
    encrypted_private_key: Optional[str] = None
    public_key_v2: Optional[str] = None
    encrypted_private_key_v2: Optional[str] = None
    models: Optional[List[ModelMinimal]] = []
    coupons: Optional[List[Coupon]] = []
    created_coupons: Optional[List[Coupon]] = []


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    """Database data schema for user"""

    hashed_password: str
    nonce: Optional[str] = None
    numerai_api_key_public_id: Optional[str] = None
    numerai_api_key_secret: Optional[str] = None


class GenericOwner(BaseModel):
    """API data schema for generic owner"""

    id: Optional[int] = None
    username: Optional[str] = None
    default_receiving_wallet_address: Optional[str] = None
    social_discord: Optional[str] = None
    social_linkedin: Optional[str] = None
    social_twitter: Optional[str] = None
    social_website: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class OrderBuyer(BaseModel):
    """API data schema for order buyer"""

    id: Optional[int] = None
    username: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True
