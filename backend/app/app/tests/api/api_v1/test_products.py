from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.tests.utils.product import create_random_product
from app.tests.utils.utils import random_lower_string


@pytest.mark.skip
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

    crud.product.remove(db, id=content["id"])
    crud.model.remove(db, id=model.id)  # type: ignore


# todo turnkey rollout
@pytest.mark.skip
def test_create_product_invalid_inputs(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product_name = random_lower_string()
    base_data = {
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

    # nagative price
    data = base_data.copy()
    data["price"] = -10
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400

    # nagative expiration_round
    data = base_data.copy()
    data["expiration_round"] = -10
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400

    # invalid on-platform currency
    data = base_data.copy()
    data["is_on_platform"] = True
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400

    # invalid on-platform price precision
    data = base_data.copy()
    data["is_on_platform"] = True
    data["currency"] = "NMR"
    data["price"] = 0.00001
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400

    # invalid off-platform currency
    data = base_data.copy()
    data["currency"] = "NMR"
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400

    # invalid off-platform precision
    data = base_data.copy()
    data["price"] = 0.001
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400

    # invalid avatar scheme
    data = base_data.copy()
    data["avatar"] = "http://example.com"
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400

    crud.model.remove(db, id=model.id)  # type: ignore


def test_search_products(client: TestClient, db: Session) -> None:
    product = create_random_product(db)
    response = client.post(
        f"{settings.API_V1_STR}/products/search",
        json={"category_id": product.category_id, "term": product.name[:5]},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert product.name == content["data"][0]["name"]

    crud.product.remove(db, id=product.id)


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


# todo turnkey rollout
@pytest.mark.skip
def test_update_product(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product = create_random_product(db, owner_id=current_user["id"])
    data = dict()

    # product_name = random_lower_string()
    # data = {
    #     "name": product_name,
    #     "price": 10,
    #     "category_id": 3,
    #     "description": "Description",
    #     "is_on_platform": False,
    #     "currency": "USD",
    # }
    # model = crud.model.create(
    #     db,
    #     obj_in=schemas.ModelCreate(
    #         id=product_name,
    #         name=product_name,
    #         tournament=8,
    #         owner_id=current_user["id"],
    #     ),
    # )
    # response = client.post(
    #     f"{settings.API_V1_STR}/products/",
    #     headers=normal_user_token_headers,
    #     json=data,
    # )
    # assert response.status_code == 200
    # content = response.json()
    # assert content["name"] == data["name"]

    # update price
    data["price"] = 20.5
    response = client.put(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    assert content["price"] == data["price"]
    assert "id" in content
    assert "owner" in content

    # invalid attempt to change owner id
    data["owner_id"] = current_user["id"] + 1
    response = client.put(
        f"{settings.API_V1_STR}/products/{content['id']}",
        headers=normal_user_token_headers,
        json=data,
    )
    content = response.json()
    assert content["owner"]["id"] == current_user["id"]

    # invalid attempt to change product name
    data["name"] = random_lower_string()  # type: ignore
    response = client.put(
        f"{settings.API_V1_STR}/products/{content['id']}",
        headers=normal_user_token_headers,
        json=data,
    )
    content = response.json()
    assert content["name"] == product.name

    # invalid attempt to change category id
    data["category_id"] = 2
    response = client.put(
        f"{settings.API_V1_STR}/products/{content['id']}",
        headers=normal_user_token_headers,
        json=data,
    )
    content = response.json()
    assert content["category"]["id"] == 3

    crud.product.remove(db, id=content["id"])
    crud.model.remove(db, id=product.model_id)  # type: ignore
