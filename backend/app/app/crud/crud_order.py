import functools
from decimal import Decimal
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi.encoders import jsonable_encoder
from numerapi import NumerAPI
from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models.order import Order
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate


def parse_sort_option(sort: Optional[str]) -> Any:
    if sort == "latest":
        return desc(Order.date_order)
    else:
        return desc(Order.id)


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def create_with_buyer(
        self, db: Session, *, obj_in: OrderCreate, buyer_id: int
    ) -> Order:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, buyer_id=buyer_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_state(
        self, db: Session, *, state: str, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(self.model)
            .filter(self.model.state == state)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self,
        db: Session,
        *,
        role: str = None,
        current_user_id: int = None,
        id: int = None,
        # category_id: int = None,
        skip: int = 0,
        limit: int = 100,
        filters: Dict = None,
        # term: str = None,
        sort: str = None,
    ) -> Any:
        # all_child_categories = crud.category.get_all_subcategories(
        #     db, category_id=category_id  # type: ignore
        # )
        # all_child_category_ids = [c[0] for c in all_child_categories]

        query_filters = []
        if id is not None:
            query_filters.append(Order.id == id)
        # if category_id is not None:
        #     query_filters.append(Order.category_id.in_(all_child_category_ids))
        # if term is not None:
        #     query_filters.append(Order.name.like("%{}%".format(term)))

        if role == "buyer":
            query_filters.append(Order.buyer_id == current_user_id)
        elif role == "seller":
            query_filters.append(Product.owner_id == current_user_id)
        else:
            query_filters.append(
                or_(
                    Order.buyer_id == current_user_id,
                    Product.owner_id == current_user_id,
                )
            )
        if isinstance(filters, dict):
            for filter_key, filter_item in filters.items():
                if filter_key == "product":
                    product_id_list = [int(i) for i in filter_item["in"]]
                    query_filters.append(Order.product_id.in_(product_id_list))
                if filter_key == "round_order":
                    round_order_list = [int(i) for i in filter_item["in"]]
                    query_filters.append(Order.round_order.in_(round_order_list))

        query = db.query(self.model)
        if role != "buyer":  # to handle filter on Product owner
            query = query.join(self.model.product, isouter=True)
        if len(query_filters) > 0:
            query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
            query = query.filter(query_filter)
        count = query.count()
        query = query.order_by(parse_sort_option(sort))
        data = query.offset(skip).limit(limit).all()

        return {"total": count, "data": data}

    def get_numerai_wallet_transactions(self, public_id: str, secret_key: str) -> Any:
        """
        Retrieve products.
        """
        query = """
                  query {
                    account {
                      username
                      walletAddress
                      walletTxns {
                        amount
                        from
                        status
                        time
                        to
                        tournament
                        txHash
                        type
                      }
                    }
                  }
                """

        api = NumerAPI(public_id=public_id, secret_key=secret_key)
        account = api.raw_query(query, authorization=True)["data"]["account"]
        wallet_transactions = account["walletTxns"]
        return wallet_transactions

    def update_payment(self, db: Session, order_json: Dict) -> None:
        if order_json["currency"] == "NMR":
            buyer = crud.user.get(db, id=order_json["buyer_id"])
            if buyer:
                numerai_wallet_transactions = self.get_numerai_wallet_transactions(
                    public_id=buyer.numerai_api_key_public_id,  # type: ignore
                    secret_key=buyer.numerai_api_key_secret,  # type: ignore
                )
                for transaction in numerai_wallet_transactions:
                    time = (
                        pd.to_datetime(transaction["time"])
                        .tz_localize(None)
                        .to_pydatetime()
                    )
                    if time < pd.to_datetime(order_json["date_order"]).to_pydatetime():
                        continue
                    if transaction["to"] == order_json["to_address"]:
                        print(
                            f"Transaction match for order {order_json['id']} "
                            f"[{buyer.username}->{order_json['product']['name']}], "
                            f"{transaction['amount']} {order_json['currency']} / "
                            f"{order_json['price']} {order_json['currency']}, status: {transaction['status']}"
                        )
                        order_obj = crud.order.get(db, id=order_json["id"])
                        if order_obj:
                            order_obj.transaction_hash = transaction["txHash"]
                            if (
                                Decimal(transaction["amount"])
                                >= Decimal(order_obj.price)
                                and transaction["status"] == "confirmed"
                            ):
                                order_obj.state = "confirmed"
                            db.commit()
                            db.refresh(order_obj)
                            break
            return
        else:
            return


order = CRUDOrder(Order)
