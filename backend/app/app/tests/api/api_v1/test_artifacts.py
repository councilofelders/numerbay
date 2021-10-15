from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.product import create_random_product


def test_generate_upload_url(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product = create_random_product(
        db, owner_id=current_user["id"], mode="file"
    )  # todo check on-platform
    product_id = product.id
    model_id = product.model.id  # type: ignore
    artifact_data = {
        "filename": "test.txt",  # todo file format requirements
        "action": "PUT",
    }

    r = client.post(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts/generate-upload-url",
        headers=normal_user_token_headers,
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
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    product = crud.product.remove(db, id=product_id)
    assert product.id == product_id
    crud.model.remove(db, id=model_id)  # type: ignore


def test_generate_download_url(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product = create_random_product(db, owner_id=current_user["id"], mode="file")
    product_id = product.id
    model_id = product.model.id  # type: ignore
    artifact_data = {
        "filename": "test.txt",  # todo file format requirements
        "action": "PUT",
    }

    r = client.post(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts/generate-upload-url",
        headers=normal_user_token_headers,
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
        f"{settings.API_V1_STR}/products/{product_id}/artifacts/{artifact.id}/generate-download-url",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200

    crud.artifact.remove(db, id=artifact.id)
    product = crud.product.remove(db, id=product_id)
    assert product.id == product_id
    crud.model.remove(db, id=model_id)  # type: ignore


def test_create_product_artifact(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product = create_random_product(db, owner_id=current_user["id"], mode="file")
    product_id = product.id
    model_id = product.model.id  # type: ignore

    url = "http://exmaple.com"  # todo validate input
    data = {"url": url}

    r = client.post(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 200
    content = r.json()
    assert "id" in content
    assert "url" in content
    assert content["url"] == url

    crud.artifact.remove(db, id=content["id"])
    product = crud.product.remove(db, id=product_id)
    assert product.id == product_id
    crud.model.remove(db, id=model_id)  # type: ignore


def test_create_product_invalid_artifact(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product = create_random_product(db, owner_id=current_user["id"], mode="file")
    product_id = product.id
    crud.product.update(db, db_obj=product, obj_in={"mode": "stake"})
    model_id = product.model.id  # type: ignore

    url = "http://exmaple.com"  # todo validate input
    data = {"url": url}

    r = client.post(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 400

    product = crud.product.remove(db, id=product_id)
    assert product.id == product_id
    crud.model.remove(db, id=model_id)  # type: ignore


def test_read_product_artifact(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product = create_random_product(db, owner_id=current_user["id"], mode="file")
    product_id = product.id

    url = "http://exmaple.com"
    data = {"url": url}  # todo validate input

    r = client.post(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 200
    content = r.json()
    assert "id" in content
    assert "url" in content
    assert content["url"] == url
    artifact_id = content["id"]

    r = client.get(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    content = r.json()
    assert content["total"] > 0

    crud.artifact.remove(db, id=artifact_id)
    product = crud.product.remove(db, id=product.id)
    assert product.id == product_id
    crud.model.remove(db, id=crud.model.get_by_name(db, name=product.name, tournament=8).id)  # type: ignore


def test_update_product_artifact(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    assert r.status_code == 200
    current_user = r.json()

    product = create_random_product(db, owner_id=current_user["id"], mode="file")
    product_id = product.id
    model_id = product.model.id  # type: ignore

    url = "http://exmaple.com"
    data = {"url": url}  # todo validate input

    r = client.post(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 200
    content = r.json()
    assert "id" in content
    assert "url" in content
    assert content["url"] == url

    # update url
    new_url = "http://test.com"
    data["url"] = new_url
    response = client.put(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts/{content['id']}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    assert content["url"] == new_url

    response = client.delete(
        f"{settings.API_V1_STR}/products/{product_id}/artifacts/{content['id']}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    product = crud.product.remove(db, id=product_id)
    assert product.id == product_id
    crud.model.remove(db, id=model_id)  # type: ignore
