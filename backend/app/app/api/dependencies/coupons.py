from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException

from app import models, schemas


def calculate_option_price(
    option: schemas.ProductOption,
    coupon: Optional[str] = None,
    coupon_obj: Optional[models.Coupon] = None,
    qty: int = 1,
    raise_exceptions: bool = True,
) -> schemas.ProductOption:
    option.price *= qty
    option.quantity *= qty  # type: ignore

    if coupon:
        if coupon_obj:
            # check expiration
            if coupon_obj.date_expiration:
                if coupon_obj.date_expiration <= datetime.utcnow():
                    option.error = "Coupon expired"
                    if raise_exceptions:
                        raise HTTPException(
                            status_code=400, detail="Coupon expired",
                        )

            # todo check applicability, state, remaining

            # check min spend
            if coupon_obj.min_spend:
                if option.price < coupon_obj.min_spend:
                    option.error = f"Requires min spend of {coupon_obj.min_spend} NMR"
                    if raise_exceptions:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Coupon requires min spend of {coupon_obj.min_spend} NMR",
                        )
                    return option

            if coupon_obj.discount_mode == "percent":
                discount = option.price * coupon_obj.discount_percent / 100  # type: ignore

                # clip max discount
                if coupon_obj.max_discount:
                    discount = min(discount, Decimal(coupon_obj.max_discount))

                if discount > 0:
                    option.special_price = option.price - discount
                    option.applied_coupon = coupon_obj.code
        else:
            # coupon not found
            option.error = "Coupon not found"
            if raise_exceptions:
                raise HTTPException(status_code=400, detail="Coupon not found")
            return option
    return option
