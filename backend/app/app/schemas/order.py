""" Data schema for order """

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import BaseModel, validator, root_validator

from app.schemas.product import Product
from app.schemas.user import OrderBuyer


# Shared properties
class OrderBase(BaseModel):
    """Base data schema for order"""

    date_order: Optional[datetime] = None
    round_order: Optional[int] = None
    rounds: Optional[List[int]] = None
    quantity: Optional[int] = None
    props: Optional[Dict] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    mode: Optional[str] = None
    stake_limit: Optional[Decimal] = None
    submit_model_id: Optional[str] = None
    submit_model_name: Optional[str] = None
    submit_state: Optional[str] = None
    last_submit_round: Optional[int] = None
    chain: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    transaction_hash: Optional[str] = None
    state: Optional[str] = None
    applied_coupon_id: Optional[int] = None
    coupon: Optional[bool] = None
    coupon_specs: Optional[Dict] = None
    buyer_public_key: Optional[str] = None
    last_reminder_date: Optional[datetime] = None

    @root_validator(pre=True)
    def set_quantity(cls, values):  # type: ignore
        """Set order quantity"""
        values_to_return = dict(**values)
        values_to_return["quantity"] = len(values["rounds"]) if values["rounds"] is not None else 0
        return values_to_return


# Properties to receive on order creation
class OrderCreate(OrderBase):
    """Create data schema for order"""

    price: Decimal
    currency: str
    mode: str
    chain: Optional[str]
    from_address: str
    to_address: str
    product_id: int


# Properties to receive on order update
class OrderUpdate(OrderBase):
    """Update data schema for order"""

    product_id: Optional[int]


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    """Base database data schema for order"""

    id: int
    date_order: datetime
    round_order: int
    price: Decimal
    currency: str
    chain: str
    product: Product

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    """API data schema for order"""

    buyer: OrderBuyer
    artifacts: Optional[List] = None

    @validator("artifacts", always=True)
    def validate_artifacts(cls, value, values):  # type: ignore  # pylint: disable=W0613
        """Filter non-pruned artifacts"""
        value_to_return = []
        for artifact in value:
            if artifact.state not in ["marked_for_pruning", "pruned"]:
                value_to_return.append(artifact)
        return value_to_return


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    """Database data schema for order"""

    buyer_id: int
