# import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.order import create_random_order
from app.tests.utils.product import create_random_product
from app.tests.utils.utils import random_lower_string


# todo turnkey rollout
# @pytest.mark.skip
def test_create_order(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=current_user["id"]),  # type: ignore
        obj_in={"numerai_wallet_address": f"0xfromaddress{random_lower_string()}"},
    )

    # Active product: accept
    product = create_random_product(db, is_on_platform=True, mode="file")
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=product.owner_id),  # type: ignore
        obj_in={"numerai_wallet_address": f"0xtoaddress{random_lower_string()}"},
    )

    order_data = {
        "id": product.id,
    }
    response = client.post(
        f"{settings.API_V1_STR}/orders/",
        headers=normal_user_token_headers,
        json=order_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["buyer"]["id"] == current_user["id"]
    assert content["product"]["id"] == product.id

    # Inactive product: reject
    crud.product.update(db, db_obj=product, obj_in={"is_active": False})
    response = client.post(
        f"{settings.API_V1_STR}/orders/",
        headers=normal_user_token_headers,
        json=order_data,
    )
    assert response.status_code == 400

    crud.order.remove(db, id=content["id"])
    crud.product.remove(db, id=product.id)
    crud.model.remove(db, id=product.model.id)  # type: ignore
    crud.user.remove(db, id=product.owner_id)  # type: ignore


# todo turnkey rollout
# @pytest.mark.skip
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

    product = create_random_product(
        db, owner_id=current_user["id"], is_on_platform=True, mode="file"
    )

    order_data = {
        "id": product.id,
    }
    response = client.post(
        f"{settings.API_V1_STR}/orders/",
        headers=normal_user_token_headers,
        json=order_data,
    )
    assert response.status_code == 400

    crud.product.remove(db, id=product.id)

    product = create_random_product(db, is_on_platform=True, mode="file")
    crud.product.update(db, db_obj=product, obj_in={"wallet": buyer_wallet})

    order_data = {
        "id": product.id,
    }
    response = client.post(
        f"{settings.API_V1_STR}/orders/",
        headers=normal_user_token_headers,
        json=order_data,
    )
    assert response.status_code == 400

    crud.product.remove(db, id=product.id)


# todo turnkey rollout
# @pytest.mark.skip
def test_order_artifact(
    client: TestClient,
    superuser_token_headers: dict,
    normal_user_token_headers: dict,
    db: Session,
) -> None:
    # Create product
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    seller_user = r.json()
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=seller_user["id"]),  # type: ignore
        obj_in={"numerai_wallet_address": f"0xtoaddress{random_lower_string()}"},
    )

    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=current_user["id"]),  # type: ignore
        obj_in={"numerai_wallet_address": f"0xfromaddress{random_lower_string()}"},
    )

    product = create_random_product(
        db, owner_id=seller_user["id"], is_on_platform=True, mode="file"
    )
    url = "http://exmaple.com"  # todo validate input
    data = {"url": url}

    # Create product artifact
    r = client.post(
        f"{settings.API_V1_STR}/products/{product.id}/artifacts",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    artifact_id = r.json()["id"]

    # Create order
    order_data = {
        "id": product.id,
    }
    response = client.post(
        f"{settings.API_V1_STR}/orders/",
        headers=normal_user_token_headers,
        json=order_data,
    )
    assert response.status_code == 200
    order = crud.order.get(db, id=response.json()["id"])
    assert order

    # List artifacts: reject
    r = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/artifacts",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403

    r = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/artifacts/{artifact_id}/generate-download-url",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403

    crud.order.update(db, db_obj=order, obj_in={"state": "confirmed"})

    # List artifacts: ok
    r = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/artifacts",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 200

    r = client.get(
        f"{settings.API_V1_STR}/products/{product.id}/artifacts/{artifact_id}/generate-download-url",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 400

    crud.artifact.remove(db, id=artifact_id)
    crud.order.remove(db, id=order.id)
    crud.product.remove(db, id=product.id)


def test_search_orders(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    order = create_random_order(db, buyer_id=current_user["id"])

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

    client.delete(
        f"{settings.API_V1_STR}/orders/{order.id}", headers=normal_user_token_headers,
    )
    client.delete(
        f"{settings.API_V1_STR}/products/{order.product_id}",
        headers=normal_user_token_headers,
    )
    crud.model.remove(db, id=order.product.model.id)  # type: ignore
    crud.user.remove(db, id=order.product.owner_id)  # type: ignore
