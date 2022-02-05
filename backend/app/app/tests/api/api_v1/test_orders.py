# import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.order import get_random_order
from app.tests.utils.product import get_random_product
from app.tests.utils.utils import random_lower_string


def test_create_order(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=current_user["id"]),  # type: ignore
        obj_in={"numerai_wallet_address": f"0xfromaddress{random_lower_string()}"},
    )

    # Active product: accept
    with get_random_product(db, is_on_platform=True, mode="file") as product:
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

        # Negative or 0 quantity: reject
        order_data["quantity"] = 0
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=superuser_token_headers,
            json=order_data,
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Order quantity must be positive"

        # Wrong quantity for category: reject
        crud.product.update(db, db_obj=product, obj_in={"category_id": 4})
        order_data["quantity"] = 2
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=superuser_token_headers,
            json=order_data,
        )
        assert response.status_code == 400
        assert (
            response.json()["detail"]
            == "This product is not per-round, order quantity must be 1"
        )

        # Inactive product: reject
        crud.product.update(
            db, db_obj=product, obj_in={"category_id": 3, "is_active": False}
        )
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=superuser_token_headers,
            json=order_data,
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "This product is not available for sale"

        crud.order.remove(db, id=content["id"])


def test_create_order_invalid_duplicated(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    with get_random_order(db, buyer_id=current_user["id"]) as order:
        crud.order.update(
            db,
            db_obj=order,
            obj_in={
                "round_order": order.round_order - 1,
                "quantity": 2,
                "state": "confirmed",
            },
        )

        product = order.product
        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,  # type: ignore
            "quantity": 1,
        }
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=normal_user_token_headers,
            json=order_data,
        )
        assert response.status_code == 400
        assert (
            response.json()["detail"]
            == "Order for this product this round already exists"
        )


def test_create_order_invalid_self(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    buyer_wallet = f"0xfromaddress{random_lower_string()}"
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=current_user["id"]),  # type: ignore
        obj_in={"numerai_wallet_address": buyer_wallet},
    )

    with get_random_product(
        db, owner_id=current_user["id"], is_on_platform=True, mode="file"
    ) as product:
        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,  # type: ignore
            "quantity": 1,
        }
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=normal_user_token_headers,
            json=order_data,
        )
        assert response.status_code == 400

    with get_random_product(db, is_on_platform=True, mode="file") as product:
        crud.product.update(db, db_obj=product, obj_in={"wallet": buyer_wallet})

        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,  # type: ignore
            "quantity": 1,
        }
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=normal_user_token_headers,
            json=order_data,
        )
        assert response.status_code == 400


def test_create_order_invalid_api_permissions(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=current_user["id"]),  # type: ignore
        obj_in={"numerai_wallet_address": f"0xfromaddress{random_lower_string()}"},
    )

    # Stake mode product
    with get_random_product(db, is_on_platform=True, mode="stake") as product:
        crud.user.update(
            db,
            db_obj=crud.user.get(db, id=product.owner_id),  # type: ignore
            obj_in={"numerai_wallet_address": f"0xtoaddress{random_lower_string()}"},
        )

        # No submit model ID: reject
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
        assert response.status_code == 400

        # No permission to upload: reject
        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,
            "quantity": 1,
            "submit_model_id": "test_model_id",
        }  # type: ignore
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=superuser_token_headers,
            json=order_data,
        )
        assert response.status_code == 403

        # No permission to stake: reject
        crud.user.update(
            db,
            db_obj=crud.user.get(db, id=current_user["id"]),  # type: ignore
            obj_in={"numerai_api_key_can_upload_submission": True},
        )

        crud.product.update(
            db, db_obj=product, obj_in={"mode": "stake_with_limit", "stake_limit": 1}
        )

        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,
            "quantity": 1,
            "submit_model_id": "test_model_id",
        }  # type: ignore
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=superuser_token_headers,
            json=order_data,
        )
        assert response.status_code == 403


def test_order_artifact(
    client: TestClient,
    superuser_token_headers: dict,
    normal_user_token_headers: dict,
    db: Session,
) -> None:
    # Create product
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    seller_user = r.json()
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=seller_user["id"]),  # type: ignore
        obj_in={"numerai_wallet_address": f"0xtoaddress{random_lower_string()}"},
    )

    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=current_user["id"]),  # type: ignore
        obj_in={"numerai_wallet_address": f"0xfromaddress{random_lower_string()}"},
    )

    with get_random_product(
        db, owner_id=seller_user["id"], is_on_platform=True, mode="file"
    ) as product:
        url = "http://exmaple.com"  # todo validate input
        data = {"url": url}

        # Create product artifact
        r = client.post(
            f"{settings.API_V1_STR}/products/{product.id}/artifacts",
            headers=normal_user_token_headers,
            json=data,
        )
        assert r.status_code == 200
        artifact_id = r.json()["id"]

        # Create order
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
        order = crud.order.get(db, id=response.json()["id"])
        assert order

        # List artifacts: reject
        r = client.get(
            f"{settings.API_V1_STR}/products/{product.id}/artifacts",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 403

        r = client.get(
            f"{settings.API_V1_STR}/products/{product.id}"
            f"/artifacts/{artifact_id}/generate-download-url",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 403

        crud.order.update(db, db_obj=order, obj_in={"state": "confirmed"})

        # List artifacts: ok
        r = client.get(
            f"{settings.API_V1_STR}/products/{product.id}/artifacts",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 200

        r = client.get(
            f"{settings.API_V1_STR}/products/{product.id}"
            f"/artifacts/{artifact_id}/generate-download-url",
            headers=superuser_token_headers,
            json=data,
        )
        assert r.status_code == 400

        crud.artifact.remove(db, id=artifact_id)
        crud.order.remove(db, id=order.id)


def test_search_buyer_orders(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    with get_random_order(db, buyer_id=current_user["id"]) as order:
        response = client.post(
            f"{settings.API_V1_STR}/orders/search",
            headers=normal_user_token_headers,
            json={"role": "buyer", "filters": {"product": {"in": [order.product_id]}}},
        )
        assert response.status_code == 200
        content = response.json()
        assert content["total"] > 0
        assert order.product.name == content["data"][0]["product"]["name"]
        assert current_user["id"] == content["data"][0]["buyer"]["id"]


def test_search_seller_orders(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    with get_random_order(db, owner_id=current_user["id"]) as order:
        response = client.post(
            f"{settings.API_V1_STR}/orders/search",
            headers=normal_user_token_headers,
            json={"role": "seller", "filters": {"product": {"in": [order.product_id]}}},
        )
        assert response.status_code == 200
        content = response.json()
        assert content["total"] > 0
        assert order.product.name == content["data"][0]["product"]["name"]

        # todo soft delete
        # response = client.delete(
        #     f"{settings.API_V1_STR}/products/{order.product_id}",
        #     headers=normal_user_token_headers,
        # )
        # assert response.status_code == 200
