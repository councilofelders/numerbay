from typing import List, Dict, Any
import functools

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from app import crud
from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def parse_sort_option(sort):
    if sort == 'latest':
        return desc(Product.id)  # todo add product date info
    elif sort == 'price-up':
        return Product.price
    elif sort == 'price-down':
        return desc(Product.price)
    elif sort == 'name-up':
        return Product.name
    elif sort == 'name-down':
        return desc(Product.name)
    else:
        return desc(Product.id)


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: ProductCreate, owner_id: int
    ) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_sku(
            self, db: Session, *, sku: int
    ) -> List[Product]:
        return db.query(self.model).filter(Product.sku == sku).first()

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(self.model)
                .filter(Product.owner_id == owner_id)
                .offset(skip)
                .limit(limit)
                .all()
        )

    def get_multi_by_category(
            self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        all_child_categories = crud.category.get_all_subcategories(db, category_id=category_id)
        all_child_category_ids = [c[0] for c in all_child_categories]
        return (
            db.query(self.model)
                .filter(Product.category_id.in_(all_child_category_ids))
                .offset(skip)
                .limit(limit)
                .all()
        )

    def search(
            self, db: Session, *, id: int = None, category_id: int = None, skip: int = 0, limit: int = 100,
            filters: Dict = None, term: str = None, sort: str = None
    ) -> Any:
        all_child_categories = crud.category.get_all_subcategories(db, category_id=category_id)
        all_child_category_ids = [c[0] for c in all_child_categories]

        query_filters = []
        if id is not None:
            query_filters.append(Product.id == id)
        if category_id is not None:
            query_filters.append(Product.category_id.in_(all_child_category_ids))
        if term is not None:
            query_filters.append(Product.name.like("%{}%".format(term)))

        if isinstance(filters, dict):
            for filter_key, filter_item in filters.items():
                if filter_key == 'user':
                    user_id_list = [int(i) for i in filter_item['in']]
                    query_filters.append(Product.owner_id.in_(user_id_list))

        query = db.query(self.model)
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


product = CRUDProduct(Product)
