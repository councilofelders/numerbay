""" Data schema for product """

from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, HttpUrl

from app.schemas.category import Category
from app.schemas.model import ModelSummary
from app.schemas.product_option import (
    ProductOption,
    ProductOptionCreate,
    ProductOptionUpdate,
)
from app.schemas.review import Review
from app.schemas.user import GenericOwner


# Shared properties
class ProductBase(BaseModel):
    """ Base data schema for product """

    avatar: Optional[HttpUrl] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    use_encryption: Optional[bool] = None
    is_ready: Optional[bool] = None
    expiration_round: Optional[int] = None
    total_num_sales: Optional[int] = None
    last_sale_price: Optional[Decimal] = None
    last_sale_price_delta: Optional[Decimal] = None
    featured_products: Optional[List[int]] = None


# Properties to receive on product creation
class ProductCreate(ProductBase):
    """ Create data schema for product """

    name: str
    category_id: int
    options: Optional[List[ProductOptionCreate]]


# Properties to receive on product update
class ProductUpdate(ProductBase):
    """ Update data schema for product """

    options: Optional[List[ProductOptionUpdate]]


# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    """ Base database data schema for product """

    id: int
    name: str
    sku: str
    category: Optional[Category]

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    """ API data schema for product """

    owner: Optional[GenericOwner] = None
    model: Optional[ModelSummary] = None
    reviews: Optional[List[Review]] = None
    options: Optional[List[ProductOption]] = None
    optionIdx: Optional[str] = "0"


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    """ Database data schema for product """

    owner_id: int
