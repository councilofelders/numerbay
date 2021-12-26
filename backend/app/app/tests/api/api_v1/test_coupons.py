from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.dependencies.coupons import generate_promo_code
from app.api.dependencies.orders import update_payment
from app.core.config import settings
from app.tests.utils.product import get_random_product
from app.tests.utils.utils import random_lower_string


def test_create_product_coupon_spec(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    product_name = "z" + random_lower_string()
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [],
                    "discount_percent": 50,
                    "max_discount": "5",
                },
            }
        ],
    }
    model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=product_name,
            name=product_name,
            tournament=8,
            owner_id=current_user["id"],
        ),
    )
    model_id = model.id
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["options"][0]["price"] == data["options"][0]["price"]  # type: ignore
    assert content["options"][0]["coupon"]  # type: ignore
    assert "id" in content
    assert (
        content["id"] in content["options"][0]["coupon_specs"]["applicable_product_ids"]
    )
    assert "model" in content
    assert content["model"]["name"] == model.name
    assert "owner" in content

    crud.product.remove(db, id=content["id"])
    model = crud.model.remove(db, id=model_id)  # type: ignore
    assert model.id == model_id


def test_create_product_invalid_coupon_spec(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    product_name = "z" + random_lower_string()

    model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=product_name,
            name=product_name,
            tournament=8,
            owner_id=current_user["id"],
        ),
    )

    # no coupon specs
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": None,
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Coupon specs must be provided"

    # no applicable_product_ids
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "discount_percent": 50,
                    "max_discount": "5",
                },  # noqa: E231
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "List of applicable product IDs must be provided in coupon specs"
    )

    # no discount_percent
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [],
                    "max_discount": "5",
                },  # noqa: E231
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Discount percentage (0-100) must be provided in coupon specs"
    )

    # no max_discount
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [],
                    "discount_percent": 50,
                },  # noqa: E231
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Max discount (in NMR) must be provided in coupon specs"
    )

    # invalid reward_min_spend
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [],
                    "discount_percent": 50,
                    "max_discount": "5",
                    "reward_min_spend": 0.5,
                },
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Min spend (in NMR) for rewarding coupon must be above 1"
    )

    # invalid applicable_product_ids
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [9999],
                    "discount_percent": 50,
                    "max_discount": "5",
                    "reward_min_spend": 1,
                },
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid applicable product ID 9999"

    # invalid discount_percent
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [],
                    "discount_percent": -1,
                    "max_discount": "5",
                    "reward_min_spend": 1,
                },
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Discount percentage must be an integer between 0-100"
    )

    # invalid max_discount
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [],
                    "discount_percent": 50,
                    "max_discount": "0",
                    "reward_min_spend": 1,
                },
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Max discount must be positive"

    # invalid min_spend
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [
            {
                "price": 10,
                "is_on_platform": True,
                "currency": "NMR",
                "mode": "file",
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [],
                    "discount_percent": 50,
                    "max_discount": "5",
                    "reward_min_spend": 1,
                    "min_spend": 0.5,
                },
            }
        ],
    }
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Coupon min spend must be above 1"

    crud.model.remove(db, id=model.id)  # type: ignore


def test_order_coupon_creation(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    current_user_obj = crud.user.get(db, id=current_user["id"])
    crud.user.update(
        db,
        db_obj=current_user_obj,  # type: ignore
        obj_in={"numerai_wallet_address": f"0xfromaddress{random_lower_string()}"},
    )
    n_coupons_initial = len(current_user_obj.coupons)  # type: ignore

    # Create product
    with get_random_product(db, is_on_platform=True, mode="file") as product:
        # Add coupon spec to product
        crud.product_option.update(
            db,
            db_obj=product.options[0],  # type: ignore
            obj_in={
                "coupon": True,
                "coupon_specs": {
                    "applicable_product_ids": [],
                    "discount_percent": 50,
                    "max_discount": "5",
                },
            },
        )

        crud.user.update(
            db,
            db_obj=crud.user.get(db, id=product.owner_id),  # type: ignore
            obj_in={"numerai_wallet_address": f"0xtoaddress{random_lower_string()}"},
        )

        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,  # type: ignore
            "quantity": 1,
        }
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=superuser_token_headers,
            json=order_data,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["buyer"]["id"] == current_user["id"]
        assert content["product"]["id"] == product.id
        assert content["quantity"] == 1

        # manual confirm order
        crud.order.update(
            db,
            db_obj=crud.order.get(db, id=content["id"]),  # type: ignore
            obj_in={"transaction_hash": random_lower_string()},
        )
        update_payment(db, order_id=content["id"])

        # check coupon
        current_user_obj = crud.user.get(db, id=current_user["id"])
        assert (len(current_user_obj.coupons) - n_coupons_initial) == 1  # type: ignore

        crud.coupon.remove(db, id=current_user_obj.coupons[-1].id)  # type: ignore
        crud.order.remove(db, id=content["id"])


def test_order_coupon_redemption(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    current_user_obj = crud.user.get(db, id=current_user["id"])
    crud.user.update(
        db,
        db_obj=current_user_obj,  # type: ignore
        obj_in={"numerai_wallet_address": f"0xfromaddress{random_lower_string()}"},
    )
    # n_coupons = len(current_user_obj.coupons)  # type: ignore

    # Create product
    with get_random_product(db, is_on_platform=True, mode="file") as product:
        with get_random_product(
            db, is_on_platform=True, mode="file"
        ) as another_product:
            crud.product_option.update(
                db, db_obj=product.options[0], obj_in={"price": 5}
            )

            # Create buyer-owned coupon applicable to product
            coupon = crud.coupon.create_with_owner(
                db,
                obj_in=schemas.CouponCreate(
                    **{
                        "date_creation": datetime.utcnow(),
                        "applicability": "specific_products",
                        "code": generate_promo_code(8),
                        "applicable_product_ids": [product.id, another_product.id],
                        "discount_mode": "percent",
                        "discount_percent": 50,
                        "max_discount": 5,
                        "min_spend": None,
                        "quantity_total": 1,
                    }
                ),
                owner_id=current_user_obj.id,  # type: ignore
            )

            crud.user.update(
                db,
                db_obj=crud.user.get(db, id=product.owner_id),  # type: ignore
                obj_in={
                    "numerai_wallet_address": f"0xtoaddress{random_lower_string()}"
                },
            )

            order_data = {
                "id": product.id,
                "option_id": product.options[0].id,  # type: ignore
                "quantity": 3,
                "coupon": coupon.code,
            }
            response = client.post(
                f"{settings.API_V1_STR}/orders/",
                headers=superuser_token_headers,
                json=order_data,
            )
            assert response.status_code == 200
            content = response.json()
            assert content["buyer"]["id"] == current_user["id"]
            assert content["product"]["id"] == product.id
            assert content["quantity"] == 3
            assert content["applied_coupon_id"] == coupon.id

            # manual confirm order
            crud.order.update(
                db,
                db_obj=crud.order.get(db, id=content["id"]),  # type: ignore
                obj_in={"transaction_hash": random_lower_string()},
            )
            update_payment(db, order_id=content["id"])

            coupon = crud.coupon.get(db, id=coupon.id)  # type: ignore
            quantity_remaining = crud.coupon.calculate_quantity_remaining(db_obj=coupon)
            assert quantity_remaining == 0

            # try to redeem again (should fail)
            # coupon = crud.coupon.get(db, id=coupon.id)
            # assert coupon is not None

            crud.user.update(
                db,
                db_obj=crud.user.get(db, id=another_product.owner_id),  # type: ignore
                obj_in={
                    "numerai_wallet_address": f"0xtoaddress{random_lower_string()}"
                },
            )

            order_data = {
                "id": another_product.id,
                "option_id": another_product.options[0].id,  # type: ignore
                "quantity": 3,
                "coupon": coupon.code,
            }
            response = client.post(
                f"{settings.API_V1_STR}/orders/",
                headers=superuser_token_headers,
                json=order_data,
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "Coupon used up"

            crud.order.remove(
                db, id=content["id"]
            )  # todo deleting coupon should not delete order

            crud.coupon.remove(db, id=coupon.id)  # type: ignore


def test_order_invalid_coupon_redemption(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    current_user_obj = crud.user.get(db, id=current_user["id"])
    crud.user.update(
        db,
        db_obj=current_user_obj,  # type: ignore
        obj_in={"numerai_wallet_address": f"0xfromaddress{random_lower_string()}"},
    )

    # Create product
    with get_random_product(db, is_on_platform=True, mode="file") as product:
        with get_random_product(
            db, is_on_platform=True, mode="file"
        ) as another_product:
            crud.product_option.update(
                db, db_obj=product.options[0], obj_in={"price": 5}
            )

            # Create buyer-owned coupon applicable to product
            coupon = crud.coupon.create_with_owner(
                db,
                obj_in=schemas.CouponCreate(
                    **{
                        "date_creation": datetime.utcnow(),
                        "applicability": "specific_products",
                        "code": generate_promo_code(8),
                        "applicable_product_ids": [product.id],
                        "discount_mode": "percent",
                        "discount_percent": 50,
                        "max_discount": 5,
                        "min_spend": 8,
                        "quantity_total": 1,
                    }
                ),
                owner_id=current_user_obj.id,  # type: ignore
            )

            crud.user.update(
                db,
                db_obj=crud.user.get(db, id=product.owner_id),  # type: ignore
                obj_in={
                    "numerai_wallet_address": f"0xtoaddress{random_lower_string()}"
                },
            )

            crud.user.update(
                db,
                db_obj=crud.user.get(db, id=another_product.owner_id),  # type: ignore
                obj_in={
                    "numerai_wallet_address": f"0xtoaddress{random_lower_string()}"
                },
            )

            # non-existent coupon
            order_data = {
                "id": product.id,
                "option_id": product.options[0].id,  # type: ignore
                "quantity": 1,
                "coupon": "WRONG",
            }
            response = client.post(
                f"{settings.API_V1_STR}/orders/",
                headers=superuser_token_headers,
                json=order_data,
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "Coupon not found"

            # not meeting min spend
            order_data = {
                "id": product.id,
                "option_id": product.options[0].id,  # type: ignore
                "quantity": 1,
                "coupon": coupon.code,
            }
            response = client.post(
                f"{settings.API_V1_STR}/orders/",
                headers=superuser_token_headers,
                json=order_data,
            )
            assert response.status_code == 400
            assert response.json()["detail"] == f"Coupon requires min spend of {8} NMR"

            # non-applicable product
            order_data = {
                "id": another_product.id,
                "option_id": another_product.options[0].id,  # type: ignore
                "quantity": 2,
                "coupon": coupon.code,
            }
            response = client.post(
                f"{settings.API_V1_STR}/orders/",
                headers=superuser_token_headers,
                json=order_data,
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "Coupon invalid"


def test_coupon_calculation(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    current_user_obj = crud.user.get(db, id=current_user["id"])

    with get_random_product(db) as product:
        crud.product_option.update(db, db_obj=product.options[0], obj_in={"price": 5})

        # Create buyer-owned coupon applicable to product
        coupon = crud.coupon.create_with_owner(
            db,
            obj_in=schemas.CouponCreate(
                **{
                    "date_creation": datetime.utcnow(),
                    "applicability": "specific_products",
                    "code": generate_promo_code(8),
                    "applicable_product_ids": [product.id],
                    "discount_mode": "percent",
                    "discount_percent": 50,
                    "max_discount": 5,
                    "min_spend": 8,
                    "quantity_total": 1,
                }
            ),
            owner_id=current_user_obj.id,  # type: ignore
        )

        # non-existent coupon
        response = client.post(
            f"{settings.API_V1_STR}/products/search-authenticated",
            json={"id": product.id, "qty": 1, "coupon": "WRONG"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert product.name == content["data"][0]["name"]
        assert content["data"][0]["options"][0]["price"] == 5
        assert content["data"][0]["options"][0]["quantity"] == 1
        assert content["data"][0]["options"][0]["special_price"] is None
        assert content["data"][0]["options"][0]["applied_coupon"] is None
        assert content["data"][0]["options"][0]["error"] == "Coupon not found"

        # not meeting min spend
        response = client.post(
            f"{settings.API_V1_STR}/products/search-authenticated",
            json={"id": product.id, "qty": 1, "coupon": coupon.code},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert product.name == content["data"][0]["name"]
        assert content["data"][0]["options"][0]["price"] == 5
        assert content["data"][0]["options"][0]["quantity"] == 1
        assert content["data"][0]["options"][0]["special_price"] is None
        assert content["data"][0]["options"][0]["applied_coupon"] is None
        assert (
            content["data"][0]["options"][0]["error"]
            == f"Requires min spend of {8} NMR"
        )

        # normal discount
        response = client.post(
            f"{settings.API_V1_STR}/products/search-authenticated",
            json={"id": product.id, "qty": 2, "coupon": coupon.code},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert product.name == content["data"][0]["name"]
        assert content["data"][0]["options"][0]["price"] == 10
        assert content["data"][0]["options"][0]["quantity"] == 2
        assert content["data"][0]["options"][0]["special_price"] == 5
        assert content["data"][0]["options"][0]["applied_coupon"] == coupon.code

        # clipped discount
        response = client.post(
            f"{settings.API_V1_STR}/products/search-authenticated",
            json={"id": product.id, "qty": 3, "coupon": coupon.code},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert product.name == content["data"][0]["name"]
        assert content["data"][0]["options"][0]["price"] == 15
        assert content["data"][0]["options"][0]["quantity"] == 3
        assert content["data"][0]["options"][0]["special_price"] == 10
        assert content["data"][0]["options"][0]["applied_coupon"] == coupon.code

        # used up coupon
        crud.coupon.update(db, db_obj=coupon, obj_in={"quantity_total": 0})
        response = client.post(
            f"{settings.API_V1_STR}/products/search-authenticated",
            json={"id": product.id, "qty": 2, "coupon": coupon.code},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert product.name == content["data"][0]["name"]
        assert content["data"][0]["options"][0]["price"] == 10
        assert content["data"][0]["options"][0]["quantity"] == 2
        assert content["data"][0]["options"][0]["special_price"] is None
        assert content["data"][0]["options"][0]["applied_coupon"] is None
        assert content["data"][0]["options"][0]["error"] == "Coupon used up"
        crud.coupon.update(db, db_obj=coupon, obj_in={"quantity_total": 1})

        # non-applicable product
        with get_random_product(db) as another_product:
            crud.product_option.update(
                db, db_obj=another_product.options[0], obj_in={"price": 5}
            )

            response = client.post(
                f"{settings.API_V1_STR}/products/search-authenticated",
                json={"id": another_product.id, "qty": 2, "coupon": coupon.code},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            content = response.json()
            assert another_product.name == content["data"][0]["name"]
            assert content["data"][0]["options"][0]["price"] == 10
            assert content["data"][0]["options"][0]["quantity"] == 2
            assert content["data"][0]["options"][0]["special_price"] is None
            assert content["data"][0]["options"][0]["applied_coupon"] is None
            assert content["data"][0]["options"][0]["error"] == "Coupon invalid"

        crud.coupon.remove(db, id=coupon.id)  # type: ignore
