import functools
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
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
                if filter_key == "active":
                    current_round = crud.globals.update_singleton(db).selling_round  # type: ignore
                    query_filters.extend(
                        [
                            Order.round_order > current_round - Order.quantity,  # type: ignore
                            Order.state == "confirmed",
                        ]
                    )

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


order = CRUDOrder(Order)
