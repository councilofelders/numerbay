from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import ProductOptionCreate
from app.schemas.model import ModelCreate
from app.schemas.product import ProductCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_decimal, random_lower_string


def create_random_product(
    db: Session,
    *,
    owner_id: Optional[int] = None,
    is_on_platform: bool = False,
    mode: Optional[str] = None,
) -> models.Product:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    name = "zzz" + random_lower_string()
    crud.model.create(
        db, obj_in=ModelCreate(id=name, name=name, tournament=8, owner_id=owner_id)
    )

    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()

    product_in = ProductCreate(
        name=name, category_id=3, description=description, options=[], id=id,
    )
    product = crud.product.create_with_owner(
        db=db,
        obj_in=product_in,
        owner_id=owner_id,
        model_id=name,
        sku=sku,
        tournament=8,
    )

    product_option_in = ProductOptionCreate(
        is_on_platform=is_on_platform,
        quantity=1,
        price=price,
        currency="NMR" if is_on_platform else "USD",
        mode=mode,
        product_id=product.id,
    )

    crud.product_option.create(db, obj_in=product_option_in)

    return crud.product.get(db, id=product.id)  # type: ignore
