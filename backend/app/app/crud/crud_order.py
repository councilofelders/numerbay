import functools
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.api.dependencies.coupons import create_coupon_for_order
from app.api.dependencies.numerai import get_numerai_wallet_transactions
from app.api.dependencies.orders import (
    send_order_confirmation_emails,
    send_order_expired_emails,
)
from app.core.celery_app import celery_app
from app.core.config import settings
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

    def get_active_orders(self, db: Session, *, round_order: int) -> List[Order]:
        query_filters = [
            self.model.round_order > round_order - self.model.quantity,  # type: ignore
            self.model.state == "confirmed",
        ]
        query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
        orders = db.query(self.model).filter(query_filter).all()
        return orders

    def get_multi_by_state(
        self, db: Session, *, state: str, round_order: Optional[int] = None
    ) -> List[Order]:
        if round_order:
            query_filters = [
                self.model.round_order == round_order,  # type: ignore
                self.model.state == state,
            ]
            query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
        else:
            query_filter = self.model.state == state
        orders = db.query(self.model).filter(query_filter).all()
        return orders

    def get_pending_submission_orders(
        self, db: Session, *, round_order: int
    ) -> List[Order]:
        query_filters = [
            self.model.round_order > round_order - self.model.quantity,  # type: ignore
            self.model.state == "confirmed",
            or_(
                self.model.submit_state.is_(None),
                self.model.submit_state != "completed",
            ),
            self.model.submit_model_id.is_not(None),  # type: ignore
        ]
        query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
        orders = db.query(self.model).filter(query_filter).all()
        return orders

    def search(
        self,
        db: Session,
        *,
        role: str = None,
        current_user_id: int = None,
        id: int = None,
        # category_id: int = None,
        skip: int = 0,
        limit: int = None,
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
        #     query_filters.append(Order.name.ilike("%{}%".format(term)))

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
                if filter_key == "round_order":  # todo multiple rounds
                    round_order_list = [int(i) for i in filter_item["in"]]
                    query_filters.append(
                        Order.round_order > round_order_list[0] - Order.quantity
                    )
                if filter_key == "state":
                    state_list = [str(i) for i in filter_item["in"]]
                    query_filters.append(Order.state.in_(state_list))

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

    def update_payment(self, db: Session, order_json: Dict) -> None:
        order_obj = crud.order.get(db, id=order_json["id"])
        if order_json["currency"] == "NMR":
            buyer = crud.user.get(db, id=order_json["buyer_id"])
            if buyer:
                try:
                    numerai_wallet_transactions = get_numerai_wallet_transactions(
                        public_id=buyer.numerai_api_key_public_id,  # type: ignore
                        secret_key=buyer.numerai_api_key_secret,  # type: ignore
                    )
                    for transaction in numerai_wallet_transactions:
                        time = (
                            pd.to_datetime(transaction["time"])
                            .tz_localize(None)
                            .to_pydatetime()
                        )
                        if (
                            time
                            < pd.to_datetime(order_json["date_order"]).to_pydatetime()
                        ):
                            continue
                        if transaction["to"] == order_json["to_address"]:
                            print(
                                f"Transaction match for order {order_json['id']} "
                                f"[{buyer.username}->{order_json['product']['name']}], "
                                f"{transaction['amount']} {order_json['currency']} / "
                                f"{order_json['price']} {order_json['currency']}, status: {transaction['status']}"
                            )

                            # existing match
                            existing_match = (
                                db.query(self.model)
                                .filter(
                                    self.model.transaction_hash == transaction["txHash"]
                                )
                                .first()
                            )
                            if existing_match is not None:
                                print(
                                    f"Transaction {transaction['txHash']} already matched, skipping... "
                                )
                                continue

                            if order_obj:
                                # Confirmed
                                order_obj.transaction_hash = transaction["txHash"]
                                if (
                                    Decimal(transaction["amount"])
                                    >= Decimal(order_obj.price)
                                    and transaction["status"] == "confirmed"
                                ):
                                    order_obj.state = "confirmed"
                                db.commit()
                                db.refresh(order_obj)

                                # Generate coupon if applicable
                                create_coupon_for_order(db, order_obj)

                                # Update product sales stats
                                crud.product.update(
                                    db,
                                    db_obj=order_obj.product,
                                    obj_in={
                                        "total_num_sales": order_obj.product.total_num_sales
                                        + 1,
                                        "last_sale_price_delta": order_obj.price
                                        - order_obj.product.last_sale_price
                                        if order_obj.product.last_sale_price
                                        else None,
                                        "last_sale_price": order_obj.price,
                                    },
                                )

                                # Upload csv artifact for order if round open
                                globals = crud.globals.update_singleton(db)
                                selling_round = globals.selling_round  # type: ignore
                                if (
                                    selling_round == globals.active_round
                                    and order_obj.submit_model_id
                                ):  # if round open
                                    print(
                                        f"Round {globals.active_round} is open, search for artifact to upload"
                                    )
                                    artifacts = crud.artifact.get_multi_by_product_round(
                                        db,
                                        product=order_obj.product,
                                        round_tournament=selling_round,
                                    )
                                    if artifacts:
                                        csv_artifacts = [
                                            artifact
                                            for artifact in artifacts
                                            if artifact.object_name.endswith(".csv")  # type: ignore
                                        ]
                                        if csv_artifacts:
                                            csv_artifact = csv_artifacts[-1]
                                            bucket = deps.get_gcs_bucket()
                                            blob = bucket.blob(csv_artifact.object_name)
                                            if blob.exists():
                                                print(
                                                    f"Uploading csv artifact {csv_artifact.object_name} for order {order_obj.id}"
                                                )
                                                celery_app.send_task(
                                                    "app.worker.upload_numerai_artifact_task",
                                                    kwargs=dict(
                                                        order_id=order_obj.id,
                                                        object_name=csv_artifact.object_name,
                                                        model_id=order_json[
                                                            "submit_model_id"
                                                        ],
                                                        numerai_api_key_public_id=buyer.numerai_api_key_public_id,
                                                        numerai_api_key_secret=buyer.numerai_api_key_secret,
                                                        tournament=order_obj.product.model.tournament,
                                                        version=1,
                                                    ),
                                                )

                                send_order_confirmation_emails(order_obj)
                                break
                except Exception:
                    pass
                # expiration
                if (
                    order_obj
                    and order_obj.state != "confirmed"
                    and datetime.now() - order_obj.date_order
                    > timedelta(minutes=settings.PENDING_ORDER_EXPIRE_MINUTES)
                ):
                    print(f"Order {order_json['id']} expired")
                    order_obj.state = "expired"
                    db.commit()
                    db.refresh(order_obj)

                    send_order_expired_emails(order_obj)
            else:  # invalid buyer
                if order_obj:
                    order_obj.state = "invalid_buyer"
                db.commit()
                db.refresh(order_obj)
            return
        else:
            if order_obj:
                order_obj.state = "invalid_currency"
            db.commit()
            db.refresh(order_obj)
            return


order = CRUDOrder(Order)
