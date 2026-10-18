import secrets
from typing import Dict

from eth_account import Account
from eth_account.messages import encode_defunct
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.api_v1.endpoints.login import _new_challenge
from app.core.config import settings
from app.tests.utils.utils import random_lower_string


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_invalid(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER + random_lower_string(),
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 400
    assert "access_token" not in tokens


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "username" in result


def test_login_nonce(client: TestClient, db: Session) -> None:
    public_address = Account.create().address
    nonce_request_data = {"public_address": public_address}
    r = client.post(f"{settings.API_V1_STR}/login/nonce", json=nonce_request_data)
    result = r.json()
    assert r.status_code == 200
    assert "nonce" in result
    assert crud.user.get_by_public_address(db, public_address=public_address) is None


def test_login_nonce_invalid_address(client: TestClient) -> None:
    nonce_request_data = {"public_address": "0xtest_address"}
    r = client.post(f"{settings.API_V1_STR}/login/nonce", json=nonce_request_data)
    assert r.status_code == 400


def test_login_nonce_authenticated(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = crud.user.get(db, id=r.json()["id"])
    eth_account = Account.create()
    crud.user.update(
        db,
        db_obj=current_user,  # type: ignore
        obj_in={"public_address": eth_account.address},  # type: ignore
    )

    r = client.get(
        f"{settings.API_V1_STR}/login/nonce",
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "nonce" in result

    crud.user.remove(db, id=current_user.id)  # type: ignore


def test_get_access_token_inactive(client: TestClient, db: Session) -> None:
    eth_account = Account.create()
    public_address = eth_account.address
    nonce = secrets.token_hex(32)
    password = random_lower_string()
    user = crud.user.create(
        db,
        obj_in=schemas.UserCreate(
            username=public_address,
            password=password,
            public_address=public_address,
            nonce=nonce,
            is_active=False,
        ),
    )
    assert user.is_active is False

    login_data = {
        "username": public_address,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400

    web3_login_data = {
        "public_address": public_address,
        "signature": random_lower_string(),
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token-web3", json=web3_login_data
    )
    tokens = r.json()
    assert r.status_code == 400
    assert "access_token" not in tokens

    message_hash = encode_defunct(text=f"I am signing my one-time nonce: {nonce}")
    signature = eth_account.sign_message(message_hash).signature.hex()
    web3_login_data = {
        "public_address": public_address,
        "signature": signature,
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token-web3", json=web3_login_data
    )
    tokens = r.json()
    assert r.status_code == 400
    assert "access_token" not in tokens

    db.refresh(user)
    assert user.is_active is False

    crud.user.remove(db, id=user.id)


def test_get_access_token_web3_malformed_signature(client: TestClient) -> None:
    public_address = Account.create().address
    web3_login_data = {
        "public_address": public_address,
        "signature": "0x01",
        "nonce": _new_challenge(public_address),
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token-web3", json=web3_login_data
    )
    tokens = r.json()
    assert r.status_code == 400
    assert "access_token" not in tokens


def test_get_access_token_web3(client: TestClient, db: Session) -> None:
    eth_account = Account.create()
    public_address = eth_account.address
    nonce_request_data = {
        "public_address": public_address,
    }
    r = client.post(f"{settings.API_V1_STR}/login/nonce", json=nonce_request_data)
    nonce = r.json()["nonce"]
    message_hash = encode_defunct(text=f"I am signing my one-time nonce: {nonce}")
    signature = eth_account.sign_message(message_hash).signature.hex()

    web3_login_data = {
        "public_address": public_address,
        "signature": signature,
        "nonce": nonce,
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token-web3", json=web3_login_data
    )
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
    assert (
        crud.user.get_by_public_address(db, public_address=public_address) is not None
    )

    crud.user.remove(
        db, id=crud.user.get_by_username(db, username=public_address).id  # type: ignore
    )
