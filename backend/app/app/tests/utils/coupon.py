from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Union

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.dependencies.coupons import generate_promo_code
from app.api.dependencies.orders import get_order_round_numbers
from app.core.config import settings


def create_random_coupon(db: Session, *, owner_id: int, **kwargs: Any) -> models.Coupon:
    coupon_json = {
        "date_creation": datetime.utcnow(),
        "applicability": "specific_products",
        "code": generate_promo_code(8),
        "applicable_product_ids": [],
        "discount_mode": "percent",
        "discount_percent": 50,
        "max_discount": 5,
        "min_spend": None,
        "quantity_total": 1,
    }
    coupon_json.update(kwargs)
    coupon = crud.coupon.create_with_owner(
        db,
        obj_in=schemas.CouponCreate(**coupon_json),
        owner_id=owner_id,
    )
    return coupon


def assert_coupon_calulation_error(
    *,
    client: TestClient,
    token_headers: dict,
    product_id: int,
    coupon_code: str,
    quantity: int = 1,
    expected_price: Union[int, float, Decimal] = 5,
    expected_special_price: Union[int, float, Decimal] = None,
    expected_applied_coupon: Optional[str] = None,
    error: Optional[str] = None,
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/products/search-authenticated",
        json={
            "id": product_id,
            "rounds": get_order_round_numbers(369, quantity),
            "coupon": coupon_code,
        },
        headers=token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["data"][0]["id"] == product_id
    assert content["data"][0]["options"][0]["price"] == expected_price
    assert content["data"][0]["options"][0]["quantity"] == quantity
    if expected_applied_coupon is not None:
        assert (
            content["data"][0]["options"][0]["applied_coupon"]
            == expected_applied_coupon
        )
    else:
        assert content["data"][0]["options"][0]["applied_coupon"] is None
    if expected_special_price is not None:
        # from app.db.session import SessionLocal
        # from fastapi.encoders import jsonable_encoder
        #
        # if error is None:
        #     db = SessionLocal()
        #     raise Exception(
        #         f"{jsonable_encoder(crud.product.get(db, id=product_id))}"
        #         f'{content["data"][0]["options"][0]} , {expected_special_price}, '
        #         f"{jsonable_encoder(crud.coupon.get_by_code(db, code=coupon_code))}"
        #     )
        assert (
            content["data"][0]["options"][0]["special_price"] == expected_special_price
        )
    else:
        assert content["data"][0]["options"][0]["special_price"] is None
    if error is not None:
        assert content["data"][0]["options"][0]["error"] == error
    else:
        assert content["data"][0]["options"][0]["error"] is None
