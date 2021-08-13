from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_get_users_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_username(
    client: TestClient, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"username": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_username(db, username=username)
    assert user
    assert user.username == created_user["username"]


# def test_get_existing_user(
#     client: TestClient, superuser_token_headers: dict, db: Session
# ) -> None:
#     username = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(username=username, password=password)
#     user = crud.user.create(db, obj_in=user_in)
#     user_id = user.id
#     r = client.get(
#         f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
#     )
#     assert 200 <= r.status_code < 300
#     api_user = r.json()
#     existing_user = crud.user.get_by_username(db, username=username)
#     assert existing_user
#     assert existing_user.username == api_user["username"]


def test_create_user_existing_username(
    client: TestClient, db: Session
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"username": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


# def test_retrieve_users(
#     client: TestClient, superuser_token_headers: dict, db: Session
# ) -> None:
#     username = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(username=username, password=password)
#     crud.user.create(db, obj_in=user_in)
#
#     username2 = random_email()
#     password2 = random_lower_string()
#     user_in2 = UserCreate(username=username2, password=password2)
#     crud.user.create(db, obj_in=user_in2)
#
#     r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
#     all_users = r.json()
#
#     assert len(all_users) > 1
#     for item in all_users:
#         assert "username" in item
