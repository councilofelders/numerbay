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
                    "discount_percent": "50",
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
                    "discount_percent": "50",
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

        # not meeting min spend
        response = client.post(
            f"{settings.API_V1_STR}/products/search-authenticated",
            json={"id": product.id, "qty": 1, "coupon": coupon.code},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert product.name == content["data"][0]["name"]
        assert content["data"][0]["options"][0]["special_price"] is None
        assert content["data"][0]["options"][0]["applied_coupon"] is None

        # normal discount
        response = client.post(
            f"{settings.API_V1_STR}/products/search-authenticated",
            json={"id": product.id, "qty": 2, "coupon": coupon.code},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert product.name == content["data"][0]["name"]
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
        assert content["data"][0]["options"][0]["special_price"] == 10
        assert content["data"][0]["options"][0]["applied_coupon"] == coupon.code

        crud.coupon.remove(db, id=coupon.id)  # type: ignore


# def test_create_product_invalid_artifact(
#     client: TestClient, normal_user_token_headers: dict, db: Session
# ) -> None:
#     r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
#     current_user = r.json()
#
#     product = create_random_product(
#         db, owner_id=current_user["id"], is_on_platform=True, mode="file"
#     )
#     product_id = product.id
#     crud.product_option.update(db, db_obj=product.options[0], obj_in={"mode": "stake"})  # type: ignore
#     model_id = product.model.id  # type: ignore
#
#     url = "http://exmaple.com"
#     data = {"url": url}
#
#     r = client.post(
#         f"{settings.API_V1_STR}/products/{product_id}/artifacts",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert r.status_code == 400
#     assert (
#         r.json()["detail"]
#         == "Stake modes require native artifact uploads for automated submissions"
#     )
#
#     product = crud.product.remove(db, id=product_id)
#     assert product.id == product_id
#     crud.model.remove(db, id=model_id)  # type: ignore
#
#
# def test_read_product_artifact(
#     client: TestClient, normal_user_token_headers: dict, db: Session
# ) -> None:
#     r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
#     current_user = r.json()
#
#     product = create_random_product(
#         db, owner_id=current_user["id"], is_on_platform=True, mode="file"
#     )
#     product_id = product.id
#
#     url = "http://exmaple.com"
#     data = {"url": url}
#
#     r = client.post(
#         f"{settings.API_V1_STR}/products/{product_id}/artifacts",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert r.status_code == 200
#     content = r.json()
#     assert "id" in content
#     assert "url" in content
#     assert content["url"] == url
#     artifact_id = content["id"]
#
#     r = client.get(
#         f"{settings.API_V1_STR}/products/{product_id}/artifacts",
#         headers=normal_user_token_headers,
#     )
#     assert r.status_code == 200
#     content = r.json()
#     assert content["total"] > 0
#
#     crud.artifact.remove(db, id=artifact_id)
#     product = crud.product.remove(db, id=product.id)
#     assert product.id == product_id
#     crud.model.remove(db, id=crud.model.get_by_name(db, name=product.name, tournament=8).id)  # type: ignore
#
#
# def test_update_product_artifact(
#     client: TestClient, normal_user_token_headers: dict, db: Session
# ) -> None:
#     r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
#     assert r.status_code == 200
#     current_user = r.json()
#
#     product = create_random_product(
#         db, owner_id=current_user["id"], is_on_platform=True, mode="file"
#     )
#     product_id = product.id
#     model_id = product.model.id  # type: ignore
#
#     url = "http://exmaple.com"
#     data = {"url": url}
#
#     r = client.post(
#         f"{settings.API_V1_STR}/products/{product_id}/artifacts",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert r.status_code == 200
#     content = r.json()
#     assert "id" in content
#     assert "url" in content
#     assert content["url"] == url
#
#     # update url
#     new_url = "http://test.com"
#     data["url"] = new_url
#     response = client.put(
#         f"{settings.API_V1_STR}/products/{product_id}/artifacts/{content['id']}",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 200
#     content = response.json()
#
#     assert content["url"] == new_url
#
#     response = client.delete(
#         f"{settings.API_V1_STR}/products/{product_id}/artifacts/{content['id']}",
#         headers=normal_user_token_headers,
#     )
#     assert response.status_code == 200
#     product = crud.product.remove(db, id=product_id)
#     assert product.id == product_id
#     crud.model.remove(db, id=model_id)  # type: ignore
