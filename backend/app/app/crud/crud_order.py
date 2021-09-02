from typing import List, Dict, Any
import functools

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app import crud
from app.crud.base import CRUDBase
from app.models.order import Order
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate


def parse_sort_option(sort):
    if sort == 'latest':
        return desc(Order.id)  # todo add order date info
    elif sort == 'price-up':
        return Order.price
    elif sort == 'price-down':
        return desc(Order.price)
    elif sort == 'name-up':
        return Order.name
    elif sort == 'name-down':
        return desc(Order.name)
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

    def get_by_sku(
            self, db: Session, *, sku: int
    ) -> List[Order]:
        return db.query(self.model).filter(Order.sku == sku).first()

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(self.model)
                .filter(Order.owner_id == owner_id)
                .offset(skip)
                .limit(limit)
                .all()
        )

    def get_multi_by_category(
            self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        all_child_categories = crud.category.get_all_subcategories(db, category_id=category_id)
        all_child_category_ids = [c[0] for c in all_child_categories]
        return (
            db.query(self.model)
                .filter(Order.category_id.in_(all_child_category_ids))
                .offset(skip)
                .limit(limit)
                .all()
        )

    def search(
            self, db: Session, *, role: str = None, current_user_id: int = None, id: int = None, category_id: int = None, skip: int = 0, limit: int = 100,
            term: str = None, sort: str = None
    ) -> Any:
        all_child_categories = crud.category.get_all_subcategories(db, category_id=category_id)
        all_child_category_ids = [c[0] for c in all_child_categories]

        query_filters = []
        if id is not None:
            query_filters.append(Order.id == id)
        if category_id is not None:
            query_filters.append(Order.category_id.in_(all_child_category_ids))
        if term is not None:
            query_filters.append(Order.name.like("%{}%".format(term)))

        if role == 'buyer':
            query_filters.append(Order.buyer_id == current_user_id)
        elif role == 'seller':
            query_filters.append(Product.owner_id == current_user_id)
        else:
            query_filters.append(or_(Order.buyer_id == current_user_id, Product.owner_id == current_user_id))
        # if isinstance(filters, dict):
        #     for filter_key, filter_item in filters.items():
        #         if filter_key == 'user':
        #             user_id_list = [int(i) for i in filter_item['in']]
        #             query_filters.append(Order.owner_id.in_(user_id_list))

        query = db.query(self.model)
        if role != 'buyer':  # to handle filter on Product owner
            query = query.join(self.model.product, isouter=True)
        if len(query_filters) > 0:
            query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
            query = query.filter(query_filter)
        count = query.count()
        query = query.order_by(parse_sort_option(sort))
        data = (
            query
                .offset(skip)
                .limit(limit)
                .all()
         )

        return {'total': count, 'data': data}


order = CRUDOrder(Order)
