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


# def test_create_order_invalid_inputs(
#     client: TestClient, normal_user_token_headers: dict, db: Session
# ) -> None:
#     r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
#     current_user = r.json()
#
#     order_name = random_lower_string()
#     base_data = {
#         "name": order_name,
#         "price": 10,
#         "category_id": 3,
#         "description": "Description",
#         "is_on_platform": False,
#         "currency": "USD",
#     }
#     model = crud.model.create(
#         db,
#         obj_in=schemas.ModelCreate(
#             id=order_name,
#             name=order_name,
#             tournament=8,
#             owner_id=current_user["id"],
#         ),
#     )
#
#     # nagative price
#     data = base_data.copy()
#     data['price'] = -10
#     response = client.post(
#         f"{settings.API_V1_STR}/orders/",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 400
#
#     # nagative expiration_round
#     data = base_data.copy()
#     data['expiration_round'] = -10
#     response = client.post(
#         f"{settings.API_V1_STR}/orders/",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 400
#
#     # invalid on-platform currency
#     data = base_data.copy()
#     data['is_on_platform'] = True
#     response = client.post(
#         f"{settings.API_V1_STR}/orders/",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 400
#
#     # invalid on-platform price precision
#     data = base_data.copy()
#     data['is_on_platform'] = True
#     data['currency'] = 'NMR'
#     data['price'] = 0.00001
#     response = client.post(
#         f"{settings.API_V1_STR}/orders/",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 400
#
#     # invalid off-platform currency
#     data = base_data.copy()
#     data['currency'] = 'NMR'
#     response = client.post(
#         f"{settings.API_V1_STR}/orders/",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 400
#
#     # invalid off-platform precision
#     data = base_data.copy()
#     data['price'] = 0.001
#     response = client.post(
#         f"{settings.API_V1_STR}/orders/",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 400
#
#     # invalid avatar scheme
#     data = base_data.copy()
#     data['avatar'] = 'http://example.com'
#     response = client.post(
#         f"{settings.API_V1_STR}/orders/",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 400
#
#     crud.model.remove(db, id=model.id)  # type: ignore


# def test_search_orders(client: TestClient, normal_user_token_headers: dict, db: Session) -> None:
#     r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
#     current_user = r.json()
#     crud.user.update(db, db_obj=crud.user.get(db, id=current_user['id']),
#                      obj_in={'numerai_wallet_address': '0xfromaddress'})
#
#     product = create_random_product(db, is_on_platform=True)
#     crud.user.update(db, db_obj=crud.user.get(db, id=product.owner_id),
#                      obj_in={'numerai_wallet_address': '0xtoaddress'})
#
#     order_data = {
#         'id': product.id,
#     }
#     response = client.post(f"{settings.API_V1_STR}/orders/", headers=normal_user_token_headers, json=order_data)
#     assert response.status_code == 200
#     content = response.json()
#     assert content["buyer"]["id"] == current_user['id']
#     assert content["product"]["id"] == product.id
#     order_id = content['id']
#
#     response = client.post(f"{settings.API_V1_STR}/orders/search", headers=normal_user_token_headers, json={
#         'role': 'buyer',
#         'filters': {'product': {'in': [product.id]}}
#     })
#     assert response.status_code == 200
#     content = response.json()
#     assert content["total"] > 0
#     assert product.name == content['data'][0]['product']['name']
#     assert current_user['id'] == content['data'][0]['buyer']['id']
#
#     client.delete(
#         f"{settings.API_V1_STR}/orders/{order_id}",
#         headers=normal_user_token_headers,
#     )
#     client.delete(
#         f"{settings.API_V1_STR}/products/{product.id}",
#         headers=normal_user_token_headers,
#     )
#     crud.model.remove(db, id=product.model.id)  # type: ignore
#     crud.user.remove(db, id=product.owner_id)  # type: ignore


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