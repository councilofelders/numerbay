from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    username: Optional[str] = None
    public_address: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: Optional[str] = None
    signature: Optional[str] = None
    nonce: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    signature: Optional[str] = None
    nonce: Optional[str] = None
    numerai_api_key_public_id: Optional[str] = None
    numerai_api_key_secret: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    numerai_api_key_public_id: Optional[str] = None


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
    nonce: Optional[str] = None
    numerai_api_key_public_id: Optional[str] = None
    numerai_api_key_secret: Optional[str] = None


class ProductOwner(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None

    class Config:
        orm_mode = True