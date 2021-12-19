import random
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas


def generate_promo_code(num_chars: int) -> str:
    code_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start : slice_start + 1]  # noqa: E203
    return code


def calculate_option_price(
    option: schemas.ProductOption,
    coupon: Optional[str] = None,
    coupon_obj: Optional[models.Coupon] = None,
    qty: int = 1,
    raise_exceptions: bool = True,
    user: Optional[models.User] = None,
) -> schemas.ProductOption:
    option.price *= qty
    option.quantity *= qty  # type: ignore

    if coupon:
        if coupon_obj:
            # user
            if not user:
                option.error = "Not authenticated"
                if raise_exceptions:
                    raise HTTPException(
                        status_code=400, detail="Not authenticated",
                    )
                return option

            # check expiration
            if coupon_obj.date_expiration:
                if coupon_obj.date_expiration <= datetime.utcnow():
                    option.error = "Coupon expired"
                    if raise_exceptions:
                        raise HTTPException(
                            status_code=400, detail="Coupon expired",
                        )
                    return option

            # todo check state, ownership
            # check ownership
            if not coupon_obj.is_owned_by_seller and coupon_obj.owner_id != user.id:
                option.error = "Coupon invalid"
                if raise_exceptions:
                    raise HTTPException(
                        status_code=400, detail="Coupon invalid",
                    )
                return option

            # check product applicability
            if (
                coupon_obj.applicable_product_ids
                and option.product_id not in coupon_obj.applicable_product_ids
            ):
                option.error = "Coupon invalid"
                if raise_exceptions:
                    raise HTTPException(
                        status_code=400, detail="Coupon invalid",
                    )
                return option

            # check remaining
            if coupon_obj.quantity_total:
                redemption_count = 0
                for redemption in coupon_obj.redemptions:  # type: ignore
                    if redemption.state != "expired":  # pending+confirmed
                        redemption_count += 1
                if redemption_count >= coupon_obj.quantity_total:
                    option.error = "Coupon used up"
                    if raise_exceptions:
                        raise HTTPException(
                            status_code=400, detail="Coupon used up",
                        )
                    return option

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


def create_coupon_for_order(
    db: Session, order_obj: models.Order
) -> Optional[models.Coupon]:
    if order_obj.coupon and order_obj.coupon_specs:
        data = {
            "date_creation": datetime.utcnow(),
            "applicability": "specific_products",
            "code": generate_promo_code(8),
            "applicable_product_ids": order_obj.coupon_specs.get(  # type: ignore
                "applicable_product_ids", []
            ),
            "discount_mode": "percent",
            "discount_percent": order_obj.coupon_specs.get("discount_percent", 0),  # type: ignore
            "max_discount": order_obj.coupon_specs.get("max_discount", None),  # type: ignore
            "min_spend": order_obj.coupon_specs.get("min_spend", None),  # type: ignore
            "quantity_total": 1,
        }
        coupon_obj = crud.coupon.create_with_owner(
            db, obj_in=schemas.CouponCreate(**data), owner_id=order_obj.buyer_id  # type: ignore
        )
        return coupon_obj
    return None
