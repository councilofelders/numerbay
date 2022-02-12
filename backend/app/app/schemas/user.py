""" Data schema for user """

from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas import Coupon

# Shared properties
from .model import ModelMinimal


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    username: Optional[str] = None
    public_address: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    public_address: Optional[str] = None
    signature: Optional[str] = None
    nonce: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    signature: Optional[str] = None
    nonce: Optional[str] = None
    numerai_api_key_public_id: Optional[str] = None
    numerai_api_key_secret: Optional[str] = None
    public_key: Optional[str] = None
    encrypted_private_key: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    numerai_api_key_public_id: Optional[str] = None
    numerai_api_key_can_upload_submission: Optional[bool] = None
    numerai_api_key_can_stake: Optional[bool] = None
    numerai_api_key_can_read_submission_info: Optional[bool] = None
    numerai_api_key_can_read_user_info: Optional[bool] = None
    numerai_wallet_address: Optional[str] = None
    public_key: Optional[str] = None
    encrypted_private_key: Optional[str] = None
    models: Optional[List[ModelMinimal]] = []
    coupons: Optional[List[Coupon]] = []


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
    nonce: Optional[str] = None
    numerai_api_key_public_id: Optional[str] = None
    numerai_api_key_secret: Optional[str] = None


class GenericOwner(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None

    class Config:
        orm_mode = True


class OrderBuyer(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None

    class Config:
        orm_mode = True
