from contextlib import contextmanager
from datetime import datetime
from typing import Generator, Optional

from eth_account import Account
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, models
from app.api.dependencies.orders import get_order_weekend_round_numbers, update_payment
from app.core.config import settings
from app.schemas import OrderCreate
from app.tests.utils.product import create_random_product
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_order(
    db: Session,
    *,
    buyer_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    mode: Optional[str] = "file",
) -> models.Order:
    if buyer_id:
        buyer = crud.user.get(db, id=buyer_id)
    else:
        buyer = create_random_user(db)
        buyer_id = buyer.id
    crud.user.update(
        db,
        db_obj=buyer,  # type: ignore
        obj_in={"numerai_wallet_address": Account.create().address},
    )

    product = create_random_product(
        db, owner_id=owner_id, is_on_platform=True, mode=mode
    )
    product_owner = crud.user.get(db, id=product.owner_id)
    crud.user.update(
        db,
        db_obj=product_owner,  # type: ignore
        obj_in={"numerai_wallet_address": Account.create().address},
    )

    new_order = OrderCreate(
        rounds=get_order_weekend_round_numbers(
            crud.globals.get_singleton(db).selling_round,  # type: ignore
            product.options[0].quantity,  # type: ignore
        ),
        date_order=datetime.now(),
        round_order=crud.globals.get_singleton(db).selling_round,  # type: ignore
        price=product.options[0].price,  # type: ignore
        currency=product.options[0].currency,  # type: ignore
        mode=mode,
        from_address=buyer.numerai_wallet_address,  # type: ignore
        to_address=product_owner.numerai_wallet_address,  # type: ignore
        product_id=product.id,
    )
    order = crud.order.create_with_buyer(
        db, obj_in=new_order, buyer_id=buyer_id
    )  # type: ignore

    return order


@contextmanager
def get_random_order(
    db: Session,
    *,
    buyer_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    mode: Optional[str] = "file",
) -> Generator:
    order = create_random_order(db, buyer_id=buyer_id, owner_id=owner_id, mode=mode)
    try:
        yield order
    finally:
        buyer_id_tmp = order.buyer_id
        owner_id_tmp = order.product.owner_id
        product_id = order.product_id
        model_id = order.product.model_id
        crud.order.remove(db, id=order.id)  # type: ignore
        if buyer_id is None:
            crud.user.remove(db, id=buyer_id_tmp)  # type: ignore
        crud.product.remove(db, id=product_id)  # type: ignore
        crud.model.remove(db, id=model_id)  # type: ignore
        if owner_id is None:
            crud.user.remove(db, id=owner_id_tmp)  # type: ignore


def place_and_confirm_order(
    *,
    client: TestClient,
    token_headers: dict,
    db: Session,
    product: models.Product,
    quantity: Optional[int] = 1,
    coupon_code: Optional[str] = None,
) -> models.Order:
    selling_round = crud.globals.get_singleton(db).selling_round  # type: ignore
    order_data = {
        "id": product.id,
        "option_id": product.options[0].id,  # type: ignore
        "rounds": get_order_weekend_round_numbers(selling_round, quantity),  # type: ignore
    }
    if coupon_code is not None:
        order_data["coupon"] = coupon_code
    response = client.post(
        f"{settings.API_V1_STR}/orders/",
        headers=token_headers,
        json=order_data,
    )
    assert response.status_code == 200
    content = response.json()

    # manual confirm order
    crud.order.update(
        db,
        db_obj=crud.order.get(db, id=content["id"]),  # type: ignore
        obj_in={
            "transaction_hash": random_lower_string(),
            "round_order": selling_round,  # type: ignore
        },
    )
    update_payment(db, order_id=content["id"])
    return crud.order.get(db, id=content["id"])  # type: ignore
