import copy
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, root_validator


class CouponBase(BaseModel):
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
    date_creation: Optional[datetime] = None
    applicability: str
    code: Optional[str] = None
    applicable_seller_id: Optional[int] = None


# Properties to receive on coupon update
class CouponUpdate(CouponBase):
    pass


# Properties shared by models stored in DB
class CouponInDBBase(CouponBase):
    id: int
    date_creation: datetime
    code: str
    applicable_seller_id: Optional[int] = None
    state: Optional[str] = None
    is_owned_by_seller: bool

    class Config:
        orm_mode = True


class CouponOwner(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Coupon(CouponInDBBase):
    owner: Optional[CouponOwner] = None
    quantity_remaining: Optional[int] = None  # todo calculate quantity_remaining

    @root_validator(pre=True)
    def set_quantity_remaining(cls, values):  # type: ignore
        values_to_return = dict(**values)
        if values["quantity_total"]:
            redemption_count = 0
            for redemption in values["redemptions"]:  # type: ignore
                if redemption["state"] != "expired":  # pending+confirmed
                    redemption_count += 1
            values_to_return["quantity_remaining"] = values["quantity_total"] - redemption_count
        return values_to_return


# Properties properties stored in DB
class CouponInDB(CouponInDBBase):
    owner_id: int
