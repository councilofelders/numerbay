from sqlalchemy.orm import Session

from app import crud
from app.schemas import ProductOptionCreate
from app.schemas.product import ProductCreate, ProductUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_decimal, random_lower_string


def test_create_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=user.id, sku=sku
    )
    product_option_in = ProductOptionCreate(
        price=price, is_on_platform=False, currency="USD", product_id=product.id
    )
    crud.product_option.create(db, obj_in=product_option_in)
    assert product.name == name
    assert product.description == description
    assert product.owner.id == user.id
    assert product.options[0].price == price  # type: ignore

    crud.product.remove(db=db, id=product.id)
    crud.user.remove(db=db, id=user.id)


def test_search_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=user.id, sku=sku
    )
    product_option_in = ProductOptionCreate(
        price=price, is_on_platform=False, currency="USD", product_id=product.id
    )
    crud.product_option.create(db, obj_in=product_option_in)

    stored_product = crud.product.search(db=db, id=product.id)
    assert stored_product
    assert stored_product["total"] == 1
    assert product.name == stored_product["data"][0].name

    stored_product = crud.product.search(db=db, term=name[:5])
    assert stored_product
    assert stored_product["total"] > 0

    stored_product = crud.product.search(db=db, filters={"user": {"in": [user.id]}})
    assert stored_product
    assert stored_product["total"] > 0

    crud.product.remove(db=db, id=product.id)
    crud.user.remove(db=db, id=user.id)


def test_get_multiple_products(db: Session) -> None:
    name = random_lower_string()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=user.id, sku=sku
    )
    stored_product = crud.product.get_multi_by_category(db=db, category_id=1)
    assert stored_product
    assert len(stored_product) > 0

    stored_product = crud.product.get_multi_by_owner(db=db, owner_id=user.id)
    assert stored_product
    assert len(stored_product) > 0

    crud.product.remove(db=db, id=product.id)
    crud.user.remove(db=db, id=user.id)


def test_get_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=user.id, sku=sku
    )
    product_option_in = ProductOptionCreate(
        price=price, is_on_platform=False, currency="USD", product_id=product.id
    )
    crud.product_option.create(db, obj_in=product_option_in)

    stored_product = crud.product.get(db=db, id=product.id)
    assert stored_product
    assert product.id == stored_product.id
    assert product.name == stored_product.name
    assert product.options[0].price == stored_product.options[0].price  # type: ignore
    assert product.description == stored_product.description
    assert product.owner.id == stored_product.owner_id

    stored_product = crud.product.get_by_sku(db=db, sku=sku)
    assert stored_product
    assert product.id == stored_product.id

    crud.product.remove(db=db, id=product.id)
    crud.user.remove(db=db, id=user.id)


def test_update_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, category_id=1, description=description, options=[]
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=user.id, sku=sku
    )
    product_option_in = ProductOptionCreate(
        price=price, is_on_platform=False, currency="USD", product_id=product.id
    )
    crud.product_option.create(db, obj_in=product_option_in)
    product = crud.product.get(db, id=product.id)  # type: ignore

    description2 = random_lower_string()
    product_update = ProductUpdate(description=description2)
    product2 = crud.product.update(db=db, db_obj=product, obj_in=product_update)
    assert product.id == product2.id
    assert product.name == product2.name
    assert product.options[0].price == product2.options[0].price  # type: ignore
    assert product2.description == description2
    assert product.owner.id == product2.owner_id

    crud.product.remove(db=db, id=product.id)
    crud.user.remove(db=db, id=user.id)


def test_expire_products(db: Session) -> None:
    name = random_lower_string()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name,
        category_id=1,
        description=description,
        expiration_round=280,
        options=[],
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=user.id, sku=sku
    )
    description2 = random_lower_string()
    product_update = ProductUpdate(description=description2)
    product2 = crud.product.update(db=db, db_obj=product, obj_in=product_update)
    assert product.id == product2.id
    assert product.name == product2.name
    assert product.expiration_round == 280
    assert product.is_active

    crud.product.bulk_expire(db, current_round=281)
    product3 = crud.product.get(db, id=product.id)
    assert product3
    assert not product3.is_active

    crud.product.remove(db=db, id=product.id)
    crud.user.remove(db=db, id=user.id)


def test_delete_product(db: Session) -> None:
    name = random_lower_string()
    price = random_decimal()
    sku = f"test-{name}"
    description = random_lower_string()
    product_in = ProductCreate(
        name=name, sku=sku, category_id=1, description=description, options=[]
    )
    user = create_random_user(db)
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=user.id, sku=sku
    )
    product_option_in = ProductOptionCreate(
        price=price, is_on_platform=False, currency="USD", product_id=product.id
    )
    crud.product_option.create(db, obj_in=product_option_in)

    product2 = crud.product.remove(db=db, id=product.id)
    product3 = crud.product.get(db=db, id=product.id)
    assert product3 is None
    assert product2.id == product.id
    assert product2.name == name
    assert product2.options[0].price == price  # type: ignore
    assert product2.description == description
    assert product2.owner.id == user.id

    crud.user.remove(db=db, id=user.id)
