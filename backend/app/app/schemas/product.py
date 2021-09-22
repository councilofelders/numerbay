from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, HttpUrl

from app.schemas.category import Category
from app.schemas.model import ModelSummary
from app.schemas.user import ProductOwner


# Shared properties
class ProductBase(BaseModel):
    is_on_platform: Optional[bool] = True
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    wallet: Optional[str] = None
    chain: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    third_party_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    expiration_round: Optional[int] = None


# Properties to receive on product creation
class ProductCreate(ProductBase):
    name: str
    is_on_platform: bool
    price: Decimal
    currency: str
    chain: Optional[str]
    category_id: int


# Properties to receive on product update
class ProductUpdate(ProductBase):
    pass


# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    id: int
    name: str
    sku: str
    is_on_platform: bool
    price: Decimal
    currency: str
    chain: Optional[str]
    category: Optional[Category]

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    owner: Optional[ProductOwner] = None
    model: Optional[ModelSummary] = None


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    owner_id: int
