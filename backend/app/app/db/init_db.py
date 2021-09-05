from decimal import Decimal

from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud.user.create(db, obj_in=user_in, is_superuser=True)  # noqa: F841

    categories = crud.category.get_multi(db)
    if not categories or len(categories) < 1:
        sub_categories_in = [
            schemas.CategoryCreate(name="Numerai", slug="numerai"),
            schemas.CategoryCreate(name="Signals", slug="signals"),
        ]
        sub_sub_categories_numerai_in = [
            schemas.CategoryCreate(name="Predictions", slug="numerai-predictions"),
            schemas.CategoryCreate(name="Models", slug="numerai-models"),
        ]
        sub_sub_categories_signals_in = [
            schemas.CategoryCreate(name="Predictions", slug="signals-predictions"),
            schemas.CategoryCreate(name="Data", slug="signals-data"),
        ]
        category_in = schemas.CategoryCreate(name="All", slug="all")
        category = crud.category.create(db, obj_in=category_in)
        sub_category_1 = crud.category.create_with_parent(
            db, obj_in=sub_categories_in[0], parent_id=category.id
        )
        sub_sub_category_numerai_1 = crud.category.create_with_parent(
            db, obj_in=sub_sub_categories_numerai_in[0], parent_id=sub_category_1.id
        )
        sub_sub_category_numerai_2 = crud.category.create_with_parent(  # noqa: F841
            db, obj_in=sub_sub_categories_numerai_in[1], parent_id=sub_category_1.id
        )
        sub_category_2 = crud.category.create_with_parent(
            db, obj_in=sub_categories_in[1], parent_id=category.id
        )
        sub_sub_category_signals_1 = crud.category.create_with_parent(  # noqa: F841
            db, obj_in=sub_sub_categories_signals_in[0], parent_id=sub_category_2.id
        )
        sub_sub_category_signals_2 = crud.category.create_with_parent(  # noqa: F841
            db, obj_in=sub_sub_categories_signals_in[1], parent_id=sub_category_2.id
        )

        products = crud.product.get_multi(db)
        if not products or len(products) < 1:
            name = "integration_test"
            model_in = schemas.ModelCreate(
                id=name, name=name, tournament=8, owner_id=user.id
            )
            model = crud.model.create(db, obj_in=model_in)  # noqa: F841

            product_in = schemas.ProductCreate(
                name="integration_test",
                price=Decimal("10.34"),
                category_id=sub_sub_category_numerai_1.id,
                currency="USD",
                is_on_platform=False,
            )
            product = crud.product.create_with_owner(  # noqa: F841
                db,
                obj_in=product_in,
                owner_id=user.id,
                sku="numerai-predictions-integration_test",
                model_id=name,
            )
