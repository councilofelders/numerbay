from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.tests.utils.product import create_random_product
from app.tests.utils.utils import random_lower_string


def test_create_product(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product_name = random_lower_string()
    data = {
        "name": product_name,
        "price": 10,
        "category_id": 3,
        "description": "Description",
        "is_on_platform": False,
        "currency": "USD",
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
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["price"] == data["price"]
    assert "id" in content
    assert "owner" in content

    client.delete(
        f"{settings.API_V1_STR}/products/{content['id']}",
        headers=normal_user_token_headers,
    )
    crud.model.remove(db, id=model.id)  # type: ignore


def test_read_product(client: TestClient, db: Session) -> None:
    product = create_random_product(db)
    response = client.get(f"{settings.API_V1_STR}/products/{product.id}",)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == product.name
    assert Decimal(str(content["price"])) == product.price
    assert content["id"] == product.id
    assert content["owner"]["id"] == product.owner_id

    crud.product.remove(db, id=product.id)
    crud.model.remove(db, id=crud.model.get_by_name(db, name=product.name).id)  # type: ignore
