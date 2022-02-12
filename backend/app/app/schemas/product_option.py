""" Data schema for product option """

from decimal import Decimal
from typing import Dict, Optional

from pydantic import BaseModel, HttpUrl


# Shared properties
class ProductOptionBase(BaseModel):
    """ Base data schema for product option """

    id: Optional[int] = None
    is_on_platform: Optional[bool] = None
    third_party_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    wallet: Optional[str] = None
    chain: Optional[str] = None
    stake_limit: Optional[Decimal] = None
    mode: Optional[str] = None
    is_active: Optional[bool] = None
    coupon: Optional[bool] = None
    coupon_specs: Optional[Dict] = None


# Properties to receive on product_option creation
class ProductOptionCreate(ProductOptionBase):
    """ Create data schema for product option """

    is_on_platform: bool
    quantity: Optional[int] = 1
    price: Decimal
    currency: str
    chain: Optional[str] = None
    product_id: Optional[int] = None


# Properties to receive on product_option update
class ProductOptionUpdate(ProductOptionBase):
    """ Update data schema for product option """


# Properties shared by models stored in DB
class ProductOptionInDBBase(ProductOptionBase):
    """ Base database data schema for product option """

    id: int
    is_on_platform: bool
    price: Decimal
    currency: str
    chain: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class ProductOption(ProductOptionInDBBase):
    """ API data schema for product option """

    special_price: Optional[Decimal] = None
    applied_coupon: Optional[str] = None
    error: Optional[str] = None
    product_id: Optional[int] = None


# Properties properties stored in DB
class ProductOptionInDB(ProductOptionInDBBase):
    """ Database data schema for product option """
