from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.schemas.category import Category
from app.schemas.model import ModelSummary
from app.schemas.user import ProductOwner


# Shared properties
class ProductBase(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[Decimal] = None
    avatar: Optional[str] = None
    third_party_url: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on product creation
class ProductCreate(ProductBase):
    name: str
    price: Decimal
    category_id: int


# Properties to receive on product update
class ProductUpdate(ProductBase):
    category_id: Optional[int]


# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    id: int
    name: str
    sku: str
    price: Decimal
    category: Category

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    owner: ProductOwner
    model: Optional[ModelSummary] = None


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    owner_id: int
