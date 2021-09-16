from datetime import datetime
from typing import Optional

from eth_account import Account

from app.schemas import OrderCreate

from app.tests.utils.product import create_random_product
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.model import ModelCreate
from app.schemas.product import ProductCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_decimal, random_lower_string


def create_random_order(
    db: Session, *, buyer_id: Optional[int] = None, owner_id: Optional[int] = None
) -> models.Order:
    if buyer_id:
        buyer = crud.user.get(db, id=buyer_id)
    else:
        buyer = create_random_user(db)
    crud.user.update(db, db_obj=buyer, obj_in={'numerai_wallet_address': Account.create().address})

    product = create_random_product(db, owner_id=owner_id, is_on_platform=True)
    product_owner = crud.user.get(db, id=product.owner_id)
    crud.user.update(db, db_obj=product_owner, obj_in={'numerai_wallet_address': Account.create().address})

    new_order = OrderCreate(
        date_order=datetime.now(),
        round_order=crud.globals.get_singleton(db).selling_round,
        price=product.price,
        currency=product.currency,
        from_address=buyer.numerai_wallet_address,
        to_address=product_owner.numerai_wallet_address,
        product_id=product.id
    )
    order = crud.order.create_with_buyer(db, obj_in=new_order, buyer_id=buyer_id)

    return order
