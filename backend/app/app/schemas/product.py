from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, HttpUrl

from app.schemas.category import Category
from app.schemas.model import ModelSummary
from app.schemas.review import Review
from app.schemas.user import ProductOwner
from app.schemas.product_option import ProductOption, ProductOptionCreate, ProductOptionUpdate


# Shared properties
class ProductBase(BaseModel):
    is_on_platform: Optional[bool] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    wallet: Optional[str] = None
    mode: Optional[str] = None
    stake_limit: Optional[Decimal] = None
    chain: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    third_party_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_ready: Optional[bool] = None
    expiration_round: Optional[int] = None
    total_num_sales: Optional[int] = None
    last_sale_price: Optional[Decimal] = None
    last_sale_price_delta: Optional[Decimal] = None
    optionIdx: Optional[str] = '0'


# Properties to receive on product creation
class ProductCreate(ProductBase):
    name: str
    is_on_platform: bool
    price: Decimal
    currency: str
    chain: Optional[str]
    category_id: int
    options: Optional[List[ProductOptionCreate]]


# Properties to receive on product update
class ProductUpdate(ProductBase):
    options: Optional[List[ProductOptionUpdate]]


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
    reviews: Optional[List[Review]] = None
    options: Optional[List[ProductOption]] = None


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    owner_id: int
