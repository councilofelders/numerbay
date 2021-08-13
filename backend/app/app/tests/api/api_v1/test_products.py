from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.product import create_random_product


def test_create_product(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = {"name": "Foo", "price": 10, "category_id": 1, "description": "Description"}
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["price"] == data["price"]
    assert "id" in content
    assert "owner" in content


def test_read_product(
    client: TestClient, db: Session
) -> None:
    product = create_random_product(db)
    response = client.get(
        f"{settings.API_V1_STR}/products/{product.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == product.name
    assert Decimal(str(content["price"])) == product.price
    assert content["id"] == product.id
    assert content["owner"]["id"] == product.owner_id
