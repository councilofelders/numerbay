from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.schemas.product import Product
from app.schemas.user import OrderBuyer


# Shared properties
class OrderBase(BaseModel):
    date_order: Optional[datetime] = None
    round_order: Optional[int] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    chain: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    transaction_hash: Optional[str] = None
    state: Optional[str] = None


# Properties to receive on order creation
class OrderCreate(OrderBase):
    price: Decimal
    currency: str
    chain: Optional[str]
    from_address: str
    to_address: str
    product_id: int


# Properties to receive on order update
class OrderUpdate(OrderBase):
    product_id: Optional[int]


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: int
    date_order: datetime
    round_order: int
    price: Decimal
    currency: str
    chain: str
    product: Product

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    buyer: OrderBuyer


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    buyer_id: int