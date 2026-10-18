from typing import Dict, Tuple

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.user import user_authentication_headers
from app.tests.utils.utils import random_email, random_lower_string
from app.utils import generate_email_verification_token


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


def test_update_username_password(
    client: TestClient, db: Session, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    user_id = current_user["id"]
    user = crud.user.get(db, id=user_id)
    assert user
    original_token_version = user.token_version
    current_password = random_lower_string()
    crud.user.update(db, db_obj=user, obj_in={"password": current_password})

    new_username = random_lower_string()
    new_password = random_lower_string()
    data = {
        "username": new_username,
        "password": new_password,
        "current_password": current_password,
    }
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    db.expire_all()
    updated_user = r.json()
    user = crud.user.get_by_username(db, username=new_username)
    assert user
    assert user.id == user_id
    assert user.username == updated_user["username"]

    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json={"username": current_user["username"]},
    )
    assert r.status_code == 403

    new_headers = user_authentication_headers(
        client=client, username=new_username, password=new_password
    )
    assert new_headers["Authorization"]

    crud.user.update(
        db,
        db_obj=user,
        obj_in={
            "username": current_user["username"],
            "token_version": original_token_version,
        },
    )


def test_update_username_conflict(
    client: TestClient, db: Session, normal_user_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    existing_user = crud.user.create(
        db, obj_in=UserCreate(username=username, password=password)
    )

    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    assert 200 <= r.status_code < 300
    # current_user = r.json()

    new_username = existing_user.username
    data = {"username": new_username}
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    updated_user = r.json()
    assert r.status_code == 400
    assert "_id" not in updated_user

    crud.user.remove(db, id=existing_user.id)


def prepare_user_with_password(
    client: TestClient, db: Session, headers: Dict[str, str]
) -> Tuple[int, str]:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    user_id = r.json()["id"]
    user = crud.user.get(db, id=user_id)
    assert user
    password = random_lower_string()
    crud.user.update(db, db_obj=user, obj_in={"password": password})
    return user_id, password


def test_update_email(
    client: TestClient, db: Session, normal_user_token_headers: Dict[str, str]
) -> None:
    user_id, current_password = prepare_user_with_password(
        client, db, normal_user_token_headers
    )

    new_email = random_email()
    data = {"email": new_email, "current_password": current_password}
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    db.expire_all()
    user = crud.user.get(db, id=user_id)
    assert user
    assert user.email == new_email
    assert user.pending_email is None

    crud.user.update(db, db_obj=user, obj_in={"email": settings.EMAIL_TEST_USER})


def test_update_email_verification_mail_disabled(
    client: TestClient,
    db: Session,
    normal_user_token_headers: Dict[str, str],
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", True)
    monkeypatch.setattr(settings, "EMAILS_ENABLED", False)

    user_id, current_password = prepare_user_with_password(
        client, db, normal_user_token_headers
    )

    new_email = random_email()
    data = {"email": new_email, "current_password": current_password}
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 503
    db.expire_all()
    user = crud.user.get(db, id=user_id)
    assert user
    assert user.email == settings.EMAIL_TEST_USER
    assert user.pending_email is None


def test_update_email_verification(
    client: TestClient,
    db: Session,
    normal_user_token_headers: Dict[str, str],
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", True)
    monkeypatch.setattr(settings, "EMAILS_ENABLED", True)
    monkeypatch.setattr(
        "app.api.api_v1.endpoints.users.send_email_verification_email",
        lambda **kwargs: None,
    )

    user_id, current_password = prepare_user_with_password(
        client, db, normal_user_token_headers
    )
    user = crud.user.get(db, id=user_id)
    assert user
    old_email = user.email

    new_email = random_email()
    data = {"email": new_email, "current_password": current_password}
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    db.expire_all()
    user = crud.user.get(db, id=user_id)
    assert user
    assert user.email == old_email
    assert user.pending_email == new_email

    token = generate_email_verification_token(user_id, new_email)
    r = client.post(f"{settings.API_V1_STR}/users/verify-email", json={"token": token})
    assert 200 <= r.status_code < 300
    db.expire_all()
    user = crud.user.get(db, id=user_id)
    assert user
    assert user.email == new_email
    assert user.pending_email is None

    r = client.post(f"{settings.API_V1_STR}/users/verify-email", json={"token": token})
    assert r.status_code == 400

    crud.user.update(db, db_obj=user, obj_in={"email": settings.EMAIL_TEST_USER})


def test_update_email_supersedes_pending(
    client: TestClient,
    db: Session,
    normal_user_token_headers: Dict[str, str],
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", True)
    monkeypatch.setattr(settings, "EMAILS_ENABLED", True)
    monkeypatch.setattr(
        "app.api.api_v1.endpoints.users.send_email_verification_email",
        lambda **kwargs: None,
    )

    user_id, current_password = prepare_user_with_password(
        client, db, normal_user_token_headers
    )

    pending_address = random_email()
    data = {"email": pending_address, "current_password": current_password}
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    stale_token = generate_email_verification_token(user_id, pending_address)

    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", False)

    direct_address = random_email()
    data = {"email": direct_address, "current_password": current_password}
    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    db.expire_all()
    user = crud.user.get(db, id=user_id)
    assert user
    assert user.email == direct_address
    assert user.pending_email is None

    r = client.post(
        f"{settings.API_V1_STR}/users/verify-email", json={"token": stale_token}
    )
    assert r.status_code == 400

    crud.user.update(db, db_obj=user, obj_in={"email": settings.EMAIL_TEST_USER})


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
