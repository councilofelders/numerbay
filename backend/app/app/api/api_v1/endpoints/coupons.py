""" Coupons endpoints """

from datetime import datetime
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies.coupons import generate_promo_code

router = APIRouter()


@router.post("/", response_model=schemas.Coupon)
def create_coupon(
    *,
    db: Session = Depends(deps.get_db),
    coupon_in: schemas.CouponCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new coupon.
    """
    # todo tests
    # validate recipient
    if not isinstance(coupon_in.username, str):
        raise HTTPException(
            status_code=400, detail="Recipient username must be provided"
        )

    recipient = crud.user.get_by_username(db, username=coupon_in.username)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient user not found")

    # validate applicable_product_ids
    if not coupon_in.applicable_product_ids or not isinstance(
        coupon_in.applicable_product_ids, list
    ):
        raise HTTPException(
            status_code=400,
            detail="List of applicable product IDs " "must be provided in coupon specs",
        )

    # validate discount
    if not coupon_in.discount_percent:
        raise HTTPException(
            status_code=400,
            detail="Discount percentage (0-100) must be provided in coupon specs",
        )

    # validate max_discount
    if not coupon_in.max_discount:
        raise HTTPException(
            status_code=400,
            detail="Max discount (in NMR) must be provided in coupon specs",
        )

    # validate product existence
    for applicable_product_id in coupon_in.applicable_product_ids:
        applicable_product_obj = crud.product.get(db, id=applicable_product_id)
        if (
            not applicable_product_obj
            or applicable_product_obj.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid applicable product ID {applicable_product_id}",
            )

    # validate discount type
    try:
        coupon_in.discount_percent = int(coupon_in.discount_percent)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Discount percentage must be an integer",
        )

    # validate discount range
    if (
        not isinstance(coupon_in.discount_percent, int)
        or coupon_in.discount_percent > 100
        or coupon_in.discount_percent < 0
    ):
        raise HTTPException(
            status_code=400,
            detail="Discount percentage must be an integer between 0-100",
        )

    # validate max_discount range
    if Decimal(coupon_in.max_discount) <= Decimal("0"):
        raise HTTPException(
            status_code=400,
            detail="Max discount must be positive",
        )

    # validate min_spend range
    if coupon_in.min_spend and Decimal(coupon_in.min_spend) < Decimal("1"):
        raise HTTPException(
            status_code=400,
            detail="Coupon min spend must be above 1",
        )

    # fill defaults and create coupon
    # todo support other coupon applicability mode and discount mode
    coupon_in.applicability = "specific_products"
    coupon_in.discount_mode = "percent"
    coupon_in.date_creation = datetime.utcnow()
    if not isinstance(coupon_in.code, str):
        coupon_in.code = generate_promo_code(8)
    else:
        coupon_in.code = coupon_in.code.upper()
    if coupon_in.quantity_total is None:
        coupon_in.quantity_total = 1

    coupon_in.creator_id = current_user.id
    coupon_in_json = jsonable_encoder(coupon_in)
    coupon_in_json.pop("username")
    coupon = crud.coupon.create_with_owner(
        db, obj_in=coupon_in_json, owner_id=recipient.id
    )

    return coupon


@router.delete("/{id}", response_model=schemas.Coupon)
def delete_coupon(
    *,
    db: Session = Depends(deps.get_db),
    id: str,  # pylint: disable=W0622
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a coupon.
    """
    coupon = crud.coupon.get(db=db, id=id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    if coupon.creator_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    coupon = crud.coupon.remove(db=db, id=id)  # type: ignore
    return coupon