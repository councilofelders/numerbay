from sqlalchemy.orm import Session

from app import crud
from app.schemas.product import ProductCreate, ProductUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_decimal, random_lower_string


def test_create_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, price=price, sku=sku, category_id=1, description=description
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(db=db, obj_in=product_in, owner_id=user.id)
    assert product.name == name
    assert product.description == description
    assert product.owner.id == user.id


def test_get_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, price=price, sku=sku, category_id=1, description=description
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(db=db, obj_in=product_in, owner_id=user.id)
    stored_product = crud.product.get(db=db, id=product.id)
    assert stored_product
    assert product.id == stored_product.id
    assert product.name == stored_product.name
    assert product.price == stored_product.price
    assert product.description == stored_product.description
    assert product.owner.id == stored_product.owner_id


def test_update_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, price=price, sku=sku, category_id=1, description=description
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(db=db, obj_in=product_in, owner_id=user.id)
    description2 = random_lower_string()
    product_update = ProductUpdate(description=description2)
    product2 = crud.product.update(db=db, db_obj=product, obj_in=product_update)
    assert product.id == product2.id
    assert product.name == product2.name
    assert product.price == product2.price
    assert product2.description == description2
    assert product.owner.id == product2.owner_id


def test_delete_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, price=price, sku=sku, category_id=1, description=description
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(db=db, obj_in=product_in, owner_id=user.id)
    product2 = crud.product.remove(db=db, id=product.id)
    product3 = crud.product.get(db=db, id=product.id)
    assert product3 is None
    assert product2.id == product.id
    assert product2.name == name
    assert product2.price == price
    assert product2.description == description
    assert product2.owner.id == user.id
