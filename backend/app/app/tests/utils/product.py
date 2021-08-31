from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.product import ProductCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_decimal, random_lower_string


def create_random_product(
    db: Session, *, owner_id: Optional[int] = None
) -> models.Product:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, price=price, sku=sku, category_id=1, description=description, id=id
    )
    return crud.product.create_with_owner(db=db, obj_in=product_in, owner_id=owner_id)
