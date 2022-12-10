# import pytest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.api.dependencies.orders import get_order_weekend_round_numbers
from app.core.config import settings
from app.schemas import ArtifactCreate
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
            "rounds": list(range(300, 300 + 1)),
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
        assert content["rounds"] == list(range(300, 300 + 1))

        # Negative or 0 quantity: reject
        order_data["rounds"] = []
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=superuser_token_headers,
            json=order_data,
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Order quantity must be positive"

        # Wrong quantity for category: reject
        crud.product.update(db, db_obj=product, obj_in={"category_id": 4})
        order_data["rounds"] = list(range(300, 300 + 2))
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
                "round_order": order.round_order - 5,
                "rounds": get_order_weekend_round_numbers(
                    order.round_order - 5,  # type: ignore
                    2,
                ),
                "state": "confirmed",
            },
        )

        product = order.product
        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,  # type: ignore
            "rounds": get_order_weekend_round_numbers(
                crud.globals.get_singleton(db).selling_round,  # type: ignore
                1,
            ),
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
            "rounds": list(range(300, 300 + 1)),
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
            "rounds": list(range(300, 300 + 1)),
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
            "rounds": list(range(300, 300 + 1)),
        }
        response = client.post(
            f"{settings.API_V1_STR}/orders/",
            headers=superuser_token_headers,
            json=order_data,
        )
        assert response.status_code == 400

        # No permission to upload: reject
        crud.user.update(
            db,
            db_obj=crud.user.get(db, id=current_user["id"]),  # type: ignore
            obj_in={"numerai_api_key_can_upload_submission": False},
        )
        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,
            "rounds": list(range(300, 300 + 1)),
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
            obj_in={
                "numerai_api_key_can_upload_submission": True,
                "numerai_api_key_can_stake": False,
            },
        )

        crud.product_option.update(
            db,
            db_obj=product.options[0],
            obj_in={"mode": "stake_with_limit", "stake_limit": 1},
        )

        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,
            "rounds": list(range(300, 300 + 1)),
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
        artifact_in = ArtifactCreate(
            product_id=product.id,
            date=datetime.utcnow(),
            round_tournament=crud.globals.get_singleton(db).selling_round,  # type: ignore
            object_name="test_order_artifact.csv",
        )
        artifact = crud.artifact.create(db=db, obj_in=artifact_in)
        artifact_id = artifact.id

        # Create order
        order_data = {
            "id": product.id,
            "option_id": product.options[0].id,  # type: ignore
            "rounds": get_order_weekend_round_numbers(
                crud.globals.get_singleton(db).selling_round, 1  # type: ignore
            ),
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
        assert r.status_code == 200

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


def test_update_order_submission_model(
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
                "state": "confirmed",
            },
        )

        with get_random_product(
            db, owner_id=current_user["id"], is_on_platform=True, mode="file"
        ) as new_product:
            new_model = new_product.model

            response = client.post(
                f"{settings.API_V1_STR}/orders/{order.id}/submission-model",
                headers=normal_user_token_headers,
                json={"model_id": new_model.id},
            )
            assert response.status_code == 200
            content = response.json()
            assert content["submit_model_id"] == new_model.id
            assert content["submit_model_name"] == new_model.name


def test_update_order_submission_model_invalid(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    with get_random_order(db, buyer_id=current_user["id"]) as order:
        # non-confirmed order
        with get_random_product(
            db, owner_id=current_user["id"], is_on_platform=True, mode="file"
        ) as new_product:
            new_model = new_product.model

            response = client.post(
                f"{settings.API_V1_STR}/orders/{order.id}/submission-model",
                headers=normal_user_token_headers,
                json={"model_id": new_model.id},
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "Order not confirmed"

        # confirm order
        crud.order.update(
            db,
            db_obj=order,
            obj_in={
                "round_order": order.round_order - 1,
                "state": "confirmed",
            },
        )

        # non-owner model
        with get_random_product(db, is_on_platform=True, mode="file") as new_product:
            new_model = new_product.model

            response = client.post(
                f"{settings.API_V1_STR}/orders/{order.id}/submission-model",
                headers=normal_user_token_headers,
                json={"model_id": new_model.id},
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "Invalid model ownership"

        # invalid model ID
        response = client.post(
            f"{settings.API_V1_STR}/orders/{order.id}/submission-model",
            headers=normal_user_token_headers,
            json={"model_id": "invalid_model_id"},
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid model ID"

        # different model tournament
        with get_random_product(
            db, owner_id=current_user["id"], is_on_platform=True, mode="file"
        ) as new_product:
            new_model = new_product.model

            new_model = crud.model.update(
                db,
                db_obj=new_model,
                obj_in={"tournament": 11},
            )

            response = client.post(
                f"{settings.API_V1_STR}/orders/{order.id}/submission-model",
                headers=normal_user_token_headers,
                json={"model_id": new_model.id},
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "Invalid model tournament"

        # stake_with_limit order
        crud.order.update(
            db,
            db_obj=crud.order.get(db, id=order.id),  # type: ignore
            obj_in={
                "mode": "stake_with_limit",
            },
        )
        with get_random_product(
            db, owner_id=current_user["id"], is_on_platform=True, mode="file"
        ) as new_product:
            new_model = new_product.model

            response = client.post(
                f"{settings.API_V1_STR}/orders/{order.id}/submission-model",
                headers=normal_user_token_headers,
                json={"model_id": new_model.id},
            )
            assert response.status_code == 400
            assert (
                response.json()["detail"]
                == "Order with stake limit cannot change submission model"
            )

    # non-buyer order
    with get_random_order(db) as order:
        with get_random_product(
            db, owner_id=current_user["id"], is_on_platform=True, mode="file"
        ) as new_product:
            new_model = new_product.model

            response = client.post(
                f"{settings.API_V1_STR}/orders/{order.id}/submission-model",
                headers=normal_user_token_headers,
                json={"model_id": new_model.id},
            )
            assert response.status_code == 403
            assert response.json()["detail"] == "Not enough permissions"


def test_cancel_order(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    with get_random_order(db, buyer_id=current_user["id"]) as order:
        crud.order.update(db, db_obj=order, obj_in={"state": "pending"})
        response = client.delete(
            f"{settings.API_V1_STR}/orders/{order.id}",
            headers=normal_user_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["state"] == "expired"
