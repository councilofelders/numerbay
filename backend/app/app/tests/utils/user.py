from contextlib import contextmanager
from typing import Dict, Generator, Optional

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    data = {"username": username, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    numerai_wallet_address = f"0xtoaddress{random_lower_string()}"
    user_in = UserCreate(
        username=email,
        email=email,
        password=password,
    )
    user = crud.user.create(db=db, obj_in=user_in)
    user = crud.user.update(
        db,
        db_obj=user,  # type: ignore
        obj_in={"numerai_wallet_address": numerai_wallet_address},
    )
    return user


@contextmanager
def get_random_user(db: Session) -> Generator:
    user = create_random_user(db)
    try:
        yield user
    finally:
        crud.user.remove(db, id=user.id)  # type: ignore


def authentication_token_from_username(
    *, client: TestClient, username: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_username(db, username=username)
    if not user:
        user_in_create = UserCreate(
            username=username, email=username, password=password
        )
        crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(
        client=client, username=username, password=password
    )


def get_current_user_from_token_headers(
    *,
    client: TestClient,
    token_headers: dict,
    db: Session,
    numerai_wallet_address: Optional[str] = None,
) -> User:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=token_headers)
    current_user = r.json()
    current_user_obj = crud.user.get(db, id=current_user["id"])

    if numerai_wallet_address is not None:
        current_user_obj = crud.user.update(
            db,
            db_obj=current_user_obj,  # type: ignore
            obj_in={"numerai_wallet_address": numerai_wallet_address},
        )
    if current_user_obj is None:
        raise ValueError("Current user does not exist")
    return current_user_obj
