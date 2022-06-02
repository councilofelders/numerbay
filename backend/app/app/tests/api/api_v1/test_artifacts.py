import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas import ArtifactCreate
from app.tests.utils.product import get_random_product


def test_generate_upload_url(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    with get_random_product(
        db, owner_id=current_user["id"], is_on_platform=True, mode="file"
    ) as product:
        product_id = product.id
        artifact_data = {
            "filename": "test.txt",
            "action": "PUT",
        }

        r = client.post(
            f"{settings.API_V1_STR}/products/{product_id}/artifacts/generate-upload-url",
            headers=superuser_token_headers,
            data=artifact_data,
        )
        assert r.status_code == 200
        content = r.json()
        assert "id" in content
        assert "url" in content
        assert content["url"]

        artifact = crud.artifact.get(db, id=content["id"])
        assert artifact

        response = client.delete(
            f"{settings.API_V1_STR}/products/{product_id}/artifacts/{artifact.id}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200


def test_generate_download_url(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    with get_random_product(
        db, owner_id=current_user["id"], is_on_platform=True, mode="file"
    ) as product:
        product_id = product.id
        artifact_data = {
            "filename": "test.txt",  # todo file format requirements
            "action": "PUT",
        }

        r = client.post(
            f"{settings.API_V1_STR}/products/{product_id}/artifacts/generate-upload-url",
            headers=superuser_token_headers,
            data=artifact_data,
        )
        assert r.status_code == 200
        content = r.json()
        assert "id" in content
        assert "url" in content
        assert content["url"]

        artifact = crud.artifact.get(db, id=content["id"])
        assert artifact

        r = client.get(
            f"{settings.API_V1_STR}/products/{product_id}"
            f"/artifacts/{artifact.id}/generate-download-url",
            headers=superuser_token_headers,
        )
        assert r.status_code == 200

        crud.artifact.remove(db, id=artifact.id)


def test_read_product_artifact(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    with get_random_product(
        db, owner_id=current_user["id"], is_on_platform=True, mode="file"
    ) as product:
        product_id = product.id
        artifact_in = ArtifactCreate(
            product_id=product_id,
            date=datetime.datetime.utcnow(),
            round_tournament=crud.globals.get_singleton(db).selling_round,  # type: ignore
            object_name="test_read_product_artifact.csv",
        )
        artifact = crud.artifact.create(db=db, obj_in=artifact_in)
        artifact_id = artifact.id

        r = client.get(
            f"{settings.API_V1_STR}/products/{product_id}/artifacts",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        content = r.json()
        assert content["total"] > 0

        crud.artifact.remove(db, id=artifact_id)
