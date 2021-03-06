from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.order import get_random_order
from app.tests.utils.product import get_random_product


def test_reviews_on_platform(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    # Active product: accept
    with get_random_order(db, buyer_id=current_user["id"], mode="file") as order:
        crud.order.update(db, db_obj=order, obj_in={"state": "confirmed"})

        review_data = {
            "product_id": order.product_id,
            "rating": 5,
            "text": "test review",
        }
        response = client.post(
            f"{settings.API_V1_STR}/reviews/",
            headers=normal_user_token_headers,
            json=review_data,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["reviewer"]["id"] == current_user["id"]
        assert content["product_id"] == order.product_id
        assert content["is_verified_order"]
        review_id = content["id"]

        # Search
        response = client.post(
            f"{settings.API_V1_STR}/reviews/search",
            headers=normal_user_token_headers,
            json={
                "product_id": order.product_id,
                "filters": {"user": {"in": [current_user["id"]]}},
            },
        )
        assert response.status_code == 200
        content = response.json()
        assert content["total"] > 0
        assert order.product_id == content["data"][0]["product_id"]
        assert current_user["id"] == content["data"][0]["reviewer"]["id"]
        assert content["data"][0]["is_verified_order"]

        # Duplicate review: reject
        response = client.post(
            f"{settings.API_V1_STR}/reviews/",
            headers=normal_user_token_headers,
            json=review_data,
        )
        assert response.status_code == 400
        assert (
            response.json()["detail"]
            == "You already reviewed this product for your most recent order"
        )

        crud.review.remove(db, id=review_id)

    # Non buyer review: accept but show as not verified
    with get_random_product(db, is_on_platform=True) as product:
        review_data = {
            "product_id": product.id,
            "rating": 5,
            "text": "test review",
        }
        response = client.post(
            f"{settings.API_V1_STR}/reviews/",
            headers=normal_user_token_headers,
            json=review_data,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["reviewer"]["id"] == current_user["id"]
        assert not content["is_verified_order"]
        review_id = content["id"]

        crud.review.remove(db, id=review_id)


def test_reviews_off_platform(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    # Active product: accept
    with get_random_product(db) as product:
        review_data = {"product_id": product.id, "rating": 5, "text": "test review"}
        response = client.post(
            f"{settings.API_V1_STR}/reviews/",
            headers=normal_user_token_headers,
            json=review_data,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["reviewer"]["id"] == current_user["id"]
        assert content["product_id"] == product.id
        assert not content["is_verified_order"]
        review_id = content["id"]

        # Search
        response = client.post(
            f"{settings.API_V1_STR}/reviews/search",
            headers=normal_user_token_headers,
            json={
                "product_id": product.id,
                "filters": {"user": {"in": [current_user["id"]]}},
            },
        )
        assert response.status_code == 200
        content = response.json()
        assert content["total"] > 0
        assert product.id == content["data"][0]["product_id"]
        assert current_user["id"] == content["data"][0]["reviewer"]["id"]
        assert not content["data"][0]["is_verified_order"]

        # Duplicate review: reject
        response = client.post(
            f"{settings.API_V1_STR}/reviews/",
            headers=normal_user_token_headers,
            json=review_data,
        )
        assert response.status_code == 400
        assert (
            response.json()["detail"]
            == "You already reviewed this product for the most recent round"
        )

        crud.review.remove(db, id=review_id)
