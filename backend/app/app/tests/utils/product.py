from contextlib import contextmanager
from typing import Any, Generator, Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import ProductOptionCreate
from app.schemas.model import ModelCreate
from app.schemas.product import ProductCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_decimal, random_lower_string


def create_random_product(
    db: Session, *, owner_id: Optional[int] = None, **kwargs: Any
) -> models.Product:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    name = random_lower_string(prefix="zzz")
    crud.model.create(
        db, obj_in=ModelCreate(id=name, name=name, tournament=8, owner_id=owner_id)
    )

    sku = f"test-{name}"
    description = random_lower_string()
    is_daily = kwargs.pop("is_daily", True)

    product_in = ProductCreate(
        name=name,
        category_id=3,
        description=description,
        is_daily=is_daily,
        options=[],
        id=id,
    )
    product = crud.product.create_with_owner(
        db=db,
        obj_in=product_in,
        owner_id=owner_id,
        model_id=name,
        sku=sku,
        tournament=8,
    )

    product_option_json = kwargs
    product_option_json["is_on_platform"] = product_option_json.get(
        "is_on_platform", False
    )
    if product_option_json["is_on_platform"]:
        product_option_json["currency"] = "NMR"
    else:
        product_option_json["currency"] = "USD"
    product_option_json["quantity"] = product_option_json.get("quantity", 1)
    product_option_json["price"] = product_option_json.get("price", random_decimal())
    product_option_json["mode"] = product_option_json.get("mode", None)
    product_option_json["product_id"] = product_option_json.get(
        "product_id", product.id
    )
    product_option_in = ProductOptionCreate(**product_option_json)

    crud.product_option.create(db, obj_in=product_option_in)

    return crud.product.get(db, id=product.id)  # type: ignore


@contextmanager
def get_random_product(
    db: Session,
    *,
    owner_id: Optional[int] = None,
    persistent: bool = False,
    **kwargs: Any,
) -> Generator:
    product = create_random_product(db, owner_id=owner_id, **kwargs)
    try:
        yield product
    finally:
        if not persistent:
            owner_id_tmp = product.owner_id
            model_id = product.model_id
            crud.product.remove(db, id=product.id)
            crud.model.remove(db, id=model_id)  # type: ignore
            if owner_id is None:
                crud.user.remove(db, id=owner_id_tmp)  # type: ignore
