from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.order import get_random_order


def test_generate_upload_url(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    with get_random_order(db, owner_id=current_user["id"]) as order:
        artifact_data = {
            "order_id": order.id,
            "filename": "test.txt",
            "action": "PUT",
        }

        r = client.post(
            f"{settings.API_V1_STR}/artifacts/generate-upload-url",
            headers=superuser_token_headers,
            data=artifact_data,
        )
        assert r.status_code == 200
        content = r.json()
        assert "id" in content
        assert "url" in content
        assert content["url"]
        assert "buyer_public_key" in content

        artifact = crud.order_artifact.get(db, id=content["id"])
        assert artifact

        response = client.delete(
            f"{settings.API_V1_STR}/artifacts/{artifact.id}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200


def test_invalid_generate_upload_url(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    artifact_data = {
        "order_id": -1,
        "filename": "test.txt",
        "action": "PUT",
    }

    response = client.post(
        f"{settings.API_V1_STR}/artifacts/generate-upload-url",
        headers=superuser_token_headers,
        data=artifact_data,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

    with get_random_order(db, buyer_id=current_user["id"]) as order:
        artifact_data = {
            "order_id": order.id,
            "filename": "test.txt",
            "action": "PUT",
        }

        response = client.post(
            f"{settings.API_V1_STR}/artifacts/generate-upload-url",
            headers=superuser_token_headers,
            data=artifact_data,
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Not enough permissions"


def test_generate_download_url(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    with get_random_order(db, owner_id=current_user["id"]) as order:
        artifact_data = {
            "order_id": order.id,
            "filename": "test.txt",
            "action": "PUT",
        }

        r = client.post(
            f"{settings.API_V1_STR}/artifacts/generate-upload-url",
            headers=superuser_token_headers,
            data=artifact_data,
        )
        assert r.status_code == 200
        content = r.json()
        assert "id" in content
        assert "url" in content
        assert content["url"]

        artifact = crud.order_artifact.get(db, id=content["id"])
        assert artifact

        r = client.get(
            f"{settings.API_V1_STR}/artifacts/{artifact.id}/generate-download-url",
            headers=superuser_token_headers,
        )
        assert r.status_code == 200

        crud.order_artifact.remove(db, id=artifact.id)  # type: ignore


def test_read_order_artifact(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    with get_random_order(db, owner_id=current_user["id"]) as order:
        artifact_data = {
            "order_id": order.id,
            "filename": "test.txt",  # todo file format requirements
            "action": "PUT",
        }

        r = client.post(
            f"{settings.API_V1_STR}/artifacts/generate-upload-url",
            headers=superuser_token_headers,
            data=artifact_data,
        )
        assert r.status_code == 200
        content = r.json()

        assert "id" in content
        assert "url" in content
        assert content["url"]
        artifact_id = content["id"]

        artifact = crud.order_artifact.get(db, id=content["id"])
        assert artifact

        r = client.get(
            f"{settings.API_V1_STR}/artifacts",
            headers=superuser_token_headers,
            params={"order_id": order.id},
        )
        assert r.status_code == 200
        content = r.json()
        assert content["total"] > 0

        crud.order_artifact.remove(db, id=artifact_id)
