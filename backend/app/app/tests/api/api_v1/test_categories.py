from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.category import create_random_category
from app.tests.utils.utils import random_lower_string


def test_create_category(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    name = random_lower_string()
    data = {
        "name": name,
        "slug": name,
    }
    response = client.post(
        f"{settings.API_V1_STR}/categories/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["slug"] == data["slug"]
    assert "id" in content

    crud.category.remove(db, id=content["id"])


def test_read_categories(client: TestClient) -> None:
    # category = create_random_category(db)
    response = client.get(f"{settings.API_V1_STR}/categories",)
    assert response.status_code == 200
    content = response.json()
    assert content
    # crud.category.remove(db, id=category.id)


def test_read_category(client: TestClient, db: Session) -> None:
    category = create_random_category(db)
    response = client.get(f"{settings.API_V1_STR}/categories/{category.id}",)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == category.id
    assert content["name"] == category.name
    crud.category.remove(db, id=category.id)
