from decimal import Decimal

from fastapi.encoders import jsonable_encoder

from app.tests.utils.order import create_random_order
from app.tests.utils.product import create_random_product
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.tests.utils.utils import random_lower_string


def test_create_order(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    crud.user.update(db, db_obj=crud.user.get(db, id=current_user['id']), obj_in={'numerai_wallet_address': '0xfromaddress'})

    product = create_random_product(db, is_on_platform=True)
    crud.user.update(db, db_obj=crud.user.get(db, id=product.owner_id),
                     obj_in={'numerai_wallet_address': '0xtoaddress'})

    order_data = {
        'id': product.id,
    }
    response = client.post(f"{settings.API_V1_STR}/orders/", headers=normal_user_token_headers, json=order_data)
    assert response.status_code == 200
    content = response.json()
    assert content["buyer"]["id"] == current_user['id']
    assert content["product"]["id"] == product.id

    client.delete(
        f"{settings.API_V1_STR}/orders/{content['id']}",
        headers=normal_user_token_headers,
    )
    client.delete(
        f"{settings.API_V1_STR}/products/{product.id}",
        headers=normal_user_token_headers,
    )
    crud.model.remove(db, id=product.model.id)  # type: ignore
    crud.user.remove(db, id=product.owner_id)  # type: ignore


def test_create_order_invalid_inputs(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    crud.user.update(db, db_obj=crud.user.get(db, id=current_user['id']),
                     obj_in={'numerai_wallet_address': '0xfromaddress'})

    product = create_random_product(db, owner_id=current_user['id'], is_on_platform=True)

    order_data = {
        'id': product.id,
    }
    response = client.post(f"{settings.API_V1_STR}/orders/", headers=normal_user_token_headers, json=order_data)
    assert response.status_code == 400

    crud.product.remove(db, id=product.id)

    product = create_random_product(db, is_on_platform=True)
    crud.product.update(db, db_obj=product, obj_in={'wallet': '0xfromaddress'})

    order_data = {
        'id': product.id,
    }
    response = client.post(f"{settings.API_V1_STR}/orders/", headers=normal_user_token_headers, json=order_data)
    assert response.status_code == 400

    crud.product.remove(db, id=product.id)


def test_search_orders(client: TestClient, normal_user_token_headers: dict, db: Session) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    order = create_random_order(db, buyer_id=current_user['id'])

    response = client.post(f"{settings.API_V1_STR}/orders/search", headers=normal_user_token_headers, json={
        'role': 'buyer',
        'filters': {'product': {'in': [order.product_id]}}
    })
    assert response.status_code == 200
    content = response.json()
    assert content["total"] > 0
    assert order.product.name == content['data'][0]['product']['name']
    assert current_user['id'] == content['data'][0]['buyer']['id']

    client.delete(
        f"{settings.API_V1_STR}/orders/{order.id}",
        headers=normal_user_token_headers,
    )
    client.delete(
        f"{settings.API_V1_STR}/products/{order.product_id}",
        headers=normal_user_token_headers,
    )
    crud.model.remove(db, id=order.product.model.id)  # type: ignore
    crud.user.remove(db, id=order.product.owner_id)  # type: ignore