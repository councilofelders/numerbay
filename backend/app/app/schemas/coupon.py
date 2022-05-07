""" Data schema for coupon """

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, root_validator


class CouponBase(BaseModel):
    """Base data schema for coupon"""

    date_expiration: Optional[date] = None
    applicability: Optional[str] = None
    applicable_product_ids: Optional[List[int]] = None
    min_spend: Optional[Decimal] = None
    max_discount: Optional[int] = None
    discount_mode: Optional[str] = None
    discount_percent: Optional[int] = None
    quantity_total: Optional[int] = None


# Properties to receive on coupon creation
class CouponCreate(CouponBase):
    """Create data schema for coupon"""

    date_creation: Optional[datetime] = None
    applicability: str
    code: Optional[str] = None
    applicable_seller_id: Optional[int] = None


# Properties to receive on coupon update
class CouponUpdate(CouponBase):
    """Update data schema for coupon"""


# Properties shared by models stored in DB
class CouponInDBBase(CouponBase):
    """Base database data schema for coupon"""

    id: int
    date_creation: datetime
    code: str
    applicable_seller_id: Optional[int] = None
    state: Optional[str] = None
    is_owned_by_seller: bool

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class CouponOwner(BaseModel):
    """API data schema for coupon owner"""

    id: Optional[int] = None
    username: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class Coupon(CouponInDBBase):
    """API data schema for coupon"""

    owner: Optional[CouponOwner] = None
    quantity_remaining: Optional[int] = None

    @root_validator(pre=True)
    def set_quantity_remaining(cls, values):  # type: ignore
        """Set coupon remaining quantity"""
        values_to_return = dict(**values)
        if values["quantity_total"] is not None:
            redemption_count = 0
            for redemption in values["redemptions"]:  # type: ignore
                if redemption.state != "expired":  # pending+confirmed
                    redemption_count += 1
            values_to_return["quantity_remaining"] = (
                values["quantity_total"] - redemption_count
            )
        return values_to_return


# Properties properties stored in DB
class CouponInDB(CouponInDBBase):
    """Database data schema for coupon"""

    owner_id: int
