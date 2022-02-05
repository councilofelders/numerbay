from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.tests.utils.product import get_random_product
from app.tests.utils.utils import random_lower_string


def test_create_product(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()

    product_name = random_lower_string()
    data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        "expiration_round": 283,
        "options": [{"price": 10, "is_on_platform": False, "currency": "USD"}],
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
    model_id = model.id
    response = client.post(
        f"{settings.API_V1_STR}/products/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["options"][0]["price"] == data["options"][0]["price"]  # type: ignore
    assert "model" in content
    assert content["model"]["name"] == model.name
    assert "id" in content
    assert "owner" in content

    crud.product.remove(db, id=content["id"])
    model = crud.model.remove(db, id=model_id)  # type: ignore
    assert model.id == model_id


def test_create_product_invalid_inputs(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    product_name = random_lower_string()
    base_data = {
        "name": product_name,
        "category_id": 3,
        "description": "Description",
        # type: ignore
        "options": [{"price": 10, "is_on_platform": False, "currency": "USD"}],
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
    model_id = model.id

    # invalid name
    data = base_data.copy()
    data["name"] = "invalid name"
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Invalid product name (should only contain "
        "alphabetic characters, numbers, dashes or underscores)"
    )

    # negative price
    data = base_data.copy()
    data["options"][0]["price"] = -10  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Price must be positive"

    # negative quantity
    data = base_data.copy()
    data["options"][0]["price"] = 10  # type: ignore
    data["options"][0]["quantity"] = -1  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Quantity must be positive"

    # invalid category quantity
    data = base_data.copy()
    data["category_id"] = 4  # type: ignore
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["quantity"] = 2  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["mode"] = "file"  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "This product is not per-round, quantity must be 1"
    )

    # negative expiration_round
    data = base_data.copy()
    data["expiration_round"] = -10
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Expiration round must be a positive integer"

    # invalid on-platform no mode
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0].pop("mode", None)  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Invalid listing mode, must be one of ['file', 'stake', 'stake_with_limit']"
    )

    # invalid on-platform invalid category mode
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["mode"] = "stake"  # type: ignore
    data["category_id"] = 4
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Stake modes are not allowed for non-submission categories"
    )

    # invalid on-platform non-existent mode
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["mode"] = "wrong_mode"  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Invalid listing mode, must be one of ['file', 'stake', 'stake_with_limit']"
    )

    # invalid on-platform currency
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["currency"] = "USD"  # type: ignore
    data["options"][0]["mode"] = "file"  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "USD is not supported for on-platform listing"

    # invalid on-platform price precision
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["mode"] = "file"  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["price"] = 0.00001  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "On-platform listing price must not exceed 4 decimal places"
    )

    # invalid on-platform too low price
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["mode"] = "file"  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["price"] = 0.9  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "On-platform listing price must be greater than 1 NMR"
    )

    # invalid on-platform stake_with_limit mode without stake limit
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["price"] = 1  # type: ignore
    data["options"][0]["mode"] = "stake_with_limit"  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Stake limit is required for 'stake_with_limit' mode"
    )

    # invalid on-platform stake_with_limit mode stake limit precision
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["mode"] = "stake_with_limit"  # type: ignore
    data["options"][0]["stake_limit"] = 1.00001  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Stake limit must not exceed 4 decimal places"

    # invalid on-platform stake_with_limit mode stake limit too low
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["mode"] = "stake_with_limit"  # type: ignore
    data["options"][0]["stake_limit"] = 0.9  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Stake limit must be greater than 1 NMR"

    # invalid on-platform chain
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = True  # type: ignore
    data["options"][0]["mode"] = "file"  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    data["options"][0]["chain"] = "ethereum"  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Specifying chain is not yet supported for on-platform listing"
    )

    # invalid off-platform currency
    data = base_data.copy()
    data["options"][0]["is_on_platform"] = False  # type: ignore
    data["options"][0]["currency"] = "NMR"  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "NMR is not supported for off-platform listing"

    # invalid off-platform precision
    data = base_data.copy()
    data["options"][0]["currency"] = "USD"  # type: ignore
    data["options"][0]["price"] = 0.001  # type: ignore
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Off-platform listing price must not exceed 2 decimal places"
    )

    # invalid avatar scheme
    data = base_data.copy()
    data["options"][0]["price"] = 1  # type: ignore
    data["avatar"] = "http://example.com"
    response = client.post(
        f"{settings.API_V1_STR}/products/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Avatar image must be a HTTPS URL"

    model = crud.model.remove(db, id=model_id)  # type: ignore
    assert model.id == model_id


def test_search_products(client: TestClient, db: Session) -> None:
    with get_random_product(db) as product:
        response = client.post(
            f"{settings.API_V1_STR}/products/search",
            json={"category_id": product.category_id, "term": product.name},
        )
        assert response.status_code == 200
        content = response.json()
        assert content["total"] > 0
        assert product.name == content["data"][0]["name"]


# def test_read_product(client: TestClient, db: Session) -> None:
#     product = create_random_product(db)
#     response = client.get(f"{settings.API_V1_STR}/products/{product.id}",)
#     assert response.status_code == 200
#     content = response.json()
#     assert content["name"] == product.name
#     assert Decimal(str(content["options"][0]["price"]))
#     == product.options[0].price  # type: ignore
#     assert content["id"] == product.id
#     assert content["owner"]["id"] == product.owner_id
#
#     crud.product.remove(db, id=product.id)
#     crud.model.remove(db, id=product.model_id)  # type: ignore
#     crud.user.remove(db, id=product.owner_id)


def test_update_product(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    with get_random_product(db, owner_id=current_user["id"]) as product:
        data = dict()  # type: ignore

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
        data["options"] = [
            {
                "id": product.options[0].id,  # type: ignore
                "price": 20.5,
            }
        ]
        response = client.put(
            f"{settings.API_V1_STR}/products/{product.id}",
            headers=normal_user_token_headers,
            json=data,
        )
        assert response.status_code == 200
        content = response.json()

        assert content["options"][0]["price"] == data["options"][0]["price"]
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
        data["category_id"] = 2  # type: ignore
        response = client.put(
            f"{settings.API_V1_STR}/products/{content['id']}",
            headers=normal_user_token_headers,
            json=data,
        )
        content = response.json()
        assert content["category"]["id"] == 3

        # todo soft delete
        # response = client.delete(
        #     f"{settings.API_V1_STR}/products/{content['id']}",
        #     headers=normal_user_token_headers,
        #     json=data,
        # )
        # assert response.status_code == 200
