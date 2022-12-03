from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.api.dependencies.orders import get_order_round_numbers
from app.core.config import settings
from app.tests.utils.coupon import assert_coupon_calulation_error, create_random_coupon
from app.tests.utils.model import create_model_for_product
from app.tests.utils.order import place_and_confirm_order
from app.tests.utils.product import get_random_product
from app.tests.utils.user import get_current_user_from_token_headers, get_random_user
from app.tests.utils.utils import random_lower_string


def test_create_product_coupon_spec(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    current_user_obj = get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
    )

    product_name = random_lower_string(prefix="z")
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
    model = create_model_for_product(
        db, product_name=product_name, owner_id=current_user_obj.id
    )
    model_id = model.id
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
    current_user_obj = get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
    )

    product_name = random_lower_string(prefix="z")
    model = create_model_for_product(
        db, product_name=product_name, owner_id=current_user_obj.id
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
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
        f"{settings.API_V1_STR}/products/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Coupon min spend must be above 1"

    crud.model.remove(db, id=model.id)  # type: ignore


def test_order_coupon_creation(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    current_user_obj = get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
        numerai_wallet_address=f"0xfromaddress{random_lower_string()}",
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

        order = place_and_confirm_order(
            client=client,
            token_headers=superuser_token_headers,
            db=db,
            product=product,
            quantity=1,
        )

        # check coupon
        current_user_obj = crud.user.get(db, id=current_user_obj.id)  # type: ignore
        assert (len(current_user_obj.coupons) - n_coupons_initial) == 1  # type: ignore

        crud.coupon.remove(db, id=current_user_obj.coupons[-1].id)  # type: ignore
        crud.order.remove(db, id=order.id)  # type: ignore


def test_order_coupon_redemption(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    current_user_obj = get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
        numerai_wallet_address=f"0xfromaddress{random_lower_string()}",
    )
    # n_coupons = len(current_user_obj.coupons)  # type: ignore

    # Create product
    with get_random_product(db, is_on_platform=True, mode="file", price=5) as product:
        with get_random_product(
            db, is_on_platform=True, mode="file"
        ) as another_product:
            # Create buyer-owned coupon applicable to product
            coupon = create_random_coupon(
                db,
                owner_id=current_user_obj.id,
                applicable_product_ids=[product.id, another_product.id],
            )

            order = place_and_confirm_order(
                client=client,
                token_headers=superuser_token_headers,
                db=db,
                product=product,
                quantity=3,
                coupon_code=coupon.code,
            )
            assert order.buyer_id == current_user_obj.id
            assert order.product_id == product.id
            assert order.quantity == 3
            assert order.applied_coupon_id == coupon.id

            coupon = crud.coupon.get(db, id=coupon.id)  # type: ignore
            quantity_remaining = crud.coupon.calculate_quantity_remaining(db_obj=coupon)
            assert quantity_remaining == 0

            # try to redeem again (should fail)
            # coupon = crud.coupon.get(db, id=coupon.id)
            # assert coupon is not None

            order_data = {
                "id": another_product.id,
                "option_id": another_product.options[0].id,  # type: ignore
                "rounds": get_order_round_numbers(
                    crud.globals.get_singleton(db).selling_round,  # type: ignore
                    3,
                ),
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
                db, id=order.id  # type: ignore
            )  # todo deleting coupon should not delete order

            crud.coupon.remove(db, id=coupon.id)  # type: ignore


def test_order_invalid_coupon_redemption(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    current_user_obj = get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
        numerai_wallet_address=f"0xfromaddress{random_lower_string()}",
    )

    # Create product
    with get_random_product(db, is_on_platform=True, mode="file", price=5) as product:
        with get_random_product(
            db, is_on_platform=True, mode="file"
        ) as another_product:
            # Create buyer-owned coupon applicable to product
            coupon = create_random_coupon(
                db,
                owner_id=current_user_obj.id,
                applicable_product_ids=[product.id],
                min_spend=8,
            )

            # non-existent coupon
            order_data = {
                "id": product.id,
                "option_id": product.options[0].id,  # type: ignore
                "rounds": get_order_round_numbers(
                    crud.globals.get_singleton(db).selling_round,  # type: ignore
                    1,
                ),
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
                "rounds": get_order_round_numbers(
                    crud.globals.get_singleton(db).selling_round,  # type: ignore
                    1,
                ),
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
                "rounds": get_order_round_numbers(
                    crud.globals.get_singleton(db).selling_round,  # type: ignore
                    2,
                ),
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
    current_user_obj = get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
    )

    with get_random_product(db, price=5, is_on_platform=True) as product:
        # Create buyer-owned coupon applicable to product
        coupon = create_random_coupon(
            db,
            owner_id=current_user_obj.id,
            applicable_product_ids=[product.id],
            min_spend=8,
        )

        # non-existent coupon
        assert_coupon_calulation_error(
            client=client,
            token_headers=superuser_token_headers,
            product_id=product.id,
            coupon_code="WRONG",
            quantity=1,
            expected_price=5,
            expected_special_price=None,
            expected_applied_coupon=None,
            error="Coupon not found",
        )

        # not meeting min spend
        assert_coupon_calulation_error(
            client=client,
            token_headers=superuser_token_headers,
            product_id=product.id,
            coupon_code=coupon.code,
            quantity=1,
            expected_price=5,
            expected_special_price=None,
            expected_applied_coupon=None,
            error=f"Requires min spend of {8} NMR",
        )

        # normal discount
        assert_coupon_calulation_error(
            client=client,
            token_headers=superuser_token_headers,
            product_id=product.id,
            coupon_code=coupon.code,
            quantity=2,
            expected_price=10,
            expected_special_price=8,
            expected_applied_coupon=coupon.code,
            error=None,
        )

        # clipped discount
        assert_coupon_calulation_error(
            client=client,
            token_headers=superuser_token_headers,
            product_id=product.id,
            coupon_code=coupon.code,
            quantity=3,
            expected_price=15,
            expected_special_price=10,
            expected_applied_coupon=coupon.code,
            error=None,
        )

        # used up coupon
        crud.coupon.update(db, db_obj=coupon, obj_in={"quantity_total": 0})
        assert_coupon_calulation_error(
            client=client,
            token_headers=superuser_token_headers,
            product_id=product.id,
            coupon_code=coupon.code,
            quantity=2,
            expected_price=10,
            expected_special_price=None,
            expected_applied_coupon=None,
            error="Coupon used up",
        )
        crud.coupon.update(db, db_obj=coupon, obj_in={"quantity_total": 1})

        # non-applicable product
        with get_random_product(db, price=5) as another_product:
            assert_coupon_calulation_error(
                client=client,
                token_headers=superuser_token_headers,
                product_id=another_product.id,
                coupon_code=coupon.code,
                quantity=2,
                expected_price=10,
                expected_special_price=None,
                expected_applied_coupon=None,
                error="Coupon invalid",
            )

        crud.coupon.remove(db, id=coupon.id)  # type: ignore


def test_coupon_calculation_min_spend(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    current_user_obj = get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
        numerai_wallet_address=f"0xfromaddress{random_lower_string()}",
    )

    with get_random_product(db, is_on_platform=True, mode="file", price=5) as product1:
        with get_random_product(
            db, owner_id=product1.owner_id, is_on_platform=True, mode="file", price=5
        ) as product2, get_random_product(
            db, is_on_platform=True, mode="file", price=5
        ) as product3:
            # Create buyer-owned coupon applicable to product1 and product2
            coupon = create_random_coupon(
                db,
                owner_id=current_user_obj.id,
                applicable_product_ids=[product1.id, product2.id],
                min_spend=8,
                creator_id=product1.owner_id,
            )

            # nothing spent, not meeting min spend
            assert_coupon_calulation_error(
                client=client,
                token_headers=superuser_token_headers,
                product_id=product1.id,
                coupon_code=coupon.code,
                quantity=1,
                expected_price=5,
                expected_special_price=None,
                expected_applied_coupon=None,
                error=f"Requires min spend of {8} NMR",
            )

            # spent on product3 (different owner), not meeting min spend
            order = place_and_confirm_order(
                client=client,
                token_headers=superuser_token_headers,
                db=db,
                product=product3,
                quantity=1,
            )

            assert_coupon_calulation_error(
                client=client,
                token_headers=superuser_token_headers,
                product_id=product1.id,
                coupon_code=coupon.code,
                quantity=1,
                expected_price=5,
                expected_special_price=None,
                expected_applied_coupon=None,
                error=f"Requires min spend of {8} NMR",
            )
            crud.order.remove(db, id=order.id)

            # spent on product2 (same owner), should meet min spend
            order = place_and_confirm_order(
                client=client,
                token_headers=superuser_token_headers,
                db=db,
                product=product2,
                quantity=1,
            )

            assert_coupon_calulation_error(
                client=client,
                token_headers=superuser_token_headers,
                product_id=product1.id,
                coupon_code=coupon.code,
                quantity=1,
                expected_price=5,
                expected_special_price=3,
                expected_applied_coupon=coupon.code,
                error=None,
            )

            crud.coupon.remove(db, id=coupon.id)  # type: ignore
            crud.order.remove(db, id=order.id)


def test_create_coupon_manually(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    current_user_obj = get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
        numerai_wallet_address=f"0xfromaddress{random_lower_string()}",
    )
    n_coupons_initial = len(current_user_obj.created_coupons)  # type: ignore

    # Create product
    with get_random_product(
        db, owner_id=current_user_obj.id, is_on_platform=True, mode="file"
    ) as product:
        # Create recipient
        with get_random_user(db) as user:
            # Create coupon
            coupon_data = {
                "coupon_in": {
                    "applicability": "specific_products",
                    "applicable_product_ids": [product.id],
                    "discount_percent": 50,
                    "quantity_total": 1,
                    "max_discount": 5,
                    "code": "TESTCODE",
                }
            }
            response = client.post(
                f"{settings.API_V1_STR}/coupons/{user.username}",
                headers=superuser_token_headers,
                json=coupon_data,
            )
            assert response.status_code == 200
            content = response.json()
            assert content["creator"]["id"] == current_user_obj.id
            assert content["owner"]["id"] == user.id
            assert content["code"] == "TESTCODE"
            assert content["quantity_total"] == 1

            # check coupon
            current_user_obj = crud.user.get(db, id=current_user_obj.id)  # type: ignore
            assert (len(current_user_obj.created_coupons) - n_coupons_initial) == 1  # type: ignore

            # Delete coupon
            response = client.delete(
                f"{settings.API_V1_STR}/coupons/{content['id']}",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200


def test_invalid_create_coupon_manually(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    get_current_user_from_token_headers(
        client=client,
        token_headers=superuser_token_headers,
        db=db,
        numerai_wallet_address=f"0xfromaddress{random_lower_string()}",
    )

    # Create non-owner product
    with get_random_product(db, is_on_platform=True, mode="file") as product:
        # Create recipient
        with get_random_user(db) as user:
            # Create coupon
            coupon_data = {
                "coupon_in": {
                    "applicability": "specific_products",
                    "applicable_product_ids": [product.id],
                    "discount_percent": 50,
                    "quantity_total": 1,
                    "max_discount": 5,
                    "code": "TESTCODE",
                }
            }
            response = client.post(
                f"{settings.API_V1_STR}/coupons/{user.username}",
                headers=superuser_token_headers,
                json=coupon_data,
            )
            assert response.status_code == 400
