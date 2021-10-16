import functools
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, nulls_last  # type: ignore
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


def parse_sort_option(sort: Optional[str]) -> Any:
    if sort == "latest":
        return desc(Review.id)
    else:
        return desc(Review.id)


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    def create_with_reviewer(
        self, db: Session, *, obj_in: ReviewCreate, reviewer_id: int,
    ) -> Review:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, reviewer_id=reviewer_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_reviewer(
        self, db: Session, *, reviewer_id: int, skip: int = 0, limit: int = None
    ) -> List[Review]:
        return (
            db.query(self.model)
            .filter(Review.reviewer_id == reviewer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_product(
        self, db: Session, *, product_id: int, skip: int = 0, limit: int = None
    ) -> List[Review]:
        return (
            db.query(self.model)
            .filter(Review.product_id == product_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self,
        db: Session,
        *,
        id: int = None,
        product_id: int = None,
        skip: int = 0,
        limit: int = None,
        filters: Dict = None,
        # term: str = None,
        sort: str = None,
    ) -> Any:
        query_filters = []
        if id is not None:
            query_filters.append(Review.id == id)
        if product_id is not None:
            query_filters.append(Review.product_id == product_id)
        # if term is not None:
        #     query_filters.append(Review.name.ilike("%{}%".format(term)))

        if isinstance(filters, dict):
            for filter_key, filter_item in filters.items():
                if filter_key == "user":
                    user_id_list = [int(i) for i in filter_item["in"]]
                    query_filters.append(Review.reviewer_id.in_(user_id_list))
                if filter_key == "round_tournament":
                    round_tournament_list = [int(i) for i in filter_item["in"]]
                    query_filters.append(
                        Review.round_tournament.in_(round_tournament_list)
                    )

        query = db.query(self.model)
        if len(query_filters) > 0:
            query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
            query = query.filter(query_filter)
        count = query.count()
        query = query.order_by(nulls_last(parse_sort_option(sort)))
        data = query.offset(skip).limit(limit).all()

        return {"total": count, "data": data}


review = CRUDReview(Review)
