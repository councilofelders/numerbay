import functools
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, func, nulls_last  # type: ignore
from sqlalchemy.orm import Session
from sqlalchemy.types import JSON, Float, Integer

from app import crud
from app.crud.base import CRUDBase
from app.models.model import Model
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def parse_sort_option(sort: Optional[str]) -> Any:
    if sort == "latest":
        return desc(Product.id)  # todo add product date info
    # elif sort == 'price-up':
    #     return Product.price
    # elif sort == 'price-down':
    #     return desc(Product.price)
    elif sort == "name-up":
        return Product.name
    elif sort == "name-down":
        return desc(Product.name)
    elif sort == "rank-best":
        return Model.latest_ranks.cast(JSON)["corr"].as_string().cast(Integer)
    elif sort == "rank-worst":
        return desc(Model.latest_ranks.cast(JSON)["corr"].as_string().cast(Integer))
    elif sort == "return3m-up":
        return Model.latest_returns.cast(JSON)["threeMonths"].as_string().cast(Float)
    elif sort == "return3m-down":
        return desc(
            Model.latest_returns.cast(JSON)["threeMonths"].as_string().cast(Float)
        )
    elif sort == "mmc-up":
        return Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float)
    elif sort == "mmc-down":
        return desc(Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float))
    elif sort == "corrmmc-up":
        return Model.latest_reps.cast(JSON)["corr"].as_string().cast(
            Float
        ) + Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float)
    elif sort == "corrmmc-down":
        return desc(
            Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
            + Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float)
        )
    elif sort == "corr2mmc-up":
        return Model.latest_reps.cast(JSON)["corr"].as_string().cast(
            Float
        ) + 2.0 * Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float)
    elif sort == "corr2mmc-down":
        return desc(
            Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
            + 2.0 * Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float)
        )
    elif sort == "stake-up":
        return Model.nmr_staked
    elif sort == "stake-down":
        return desc(Model.nmr_staked)
    else:
        return Model.latest_ranks.cast(JSON)["corr"].as_string().cast(Integer)


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create_with_owner(
        self,
        db: Session,
        *,
        obj_in: ProductCreate,
        owner_id: int,
        sku: str,
        model_id: str = None,
    ) -> Product:
        obj_in_data = jsonable_encoder(obj_in)

        if model_id is None:
            model = crud.model.get_by_name(db, name=obj_in.name)
            if model:
                model_id = model.id
        db_obj = self.model(
            **obj_in_data, owner_id=owner_id, model_id=model_id, sku=sku
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_sku(self, db: Session, *, sku: str) -> Product:
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
        all_child_categories = crud.category.get_all_subcategories(
            db, category_id=category_id
        )
        all_child_category_ids = [c[0] for c in all_child_categories]
        return (
            db.query(self.model)
            .filter(Product.category_id.in_(all_child_category_ids))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def bulk_expire(self, db: Session, current_round: int) -> None:
        products_to_expire = (
            db.query(self.model).filter(Product.expiration_round < current_round).all()
        )
        for product in products_to_expire:
            product.is_active = False

        db.commit()

    def search(
        self,
        db: Session,
        *,
        id: int = None,
        category_id: int = None,
        skip: int = 0,
        limit: int = 100,
        filters: Dict = None,
        term: str = None,
        sort: str = None,
    ) -> Any:
        all_child_categories = crud.category.get_all_subcategories(db, category_id=category_id)  # type: ignore
        all_child_category_ids = [c[0] for c in all_child_categories]

        query_filters = []
        if id is not None:
            query_filters.append(Product.id == id)
        if category_id is not None:
            query_filters.append(Product.category_id.in_(all_child_category_ids))
        if term is not None:
            query_filters.append(Product.name.like("%{}%".format(term)))

        stake_step = 1
        return3m_step = 0.01

        if isinstance(filters, dict):
            for filter_key, filter_item in filters.items():
                if filter_key == "user":
                    user_id_list = [int(i) for i in filter_item["in"]]
                    query_filters.append(Product.owner_id.in_(user_id_list))
                if filter_key == "rank":
                    try:
                        if len(filter_item["in"]) > 0:
                            rank_range = filter_item["in"][0]
                            if isinstance(rank_range, str):
                                rank_range = rank_range.split(",")
                            rank_from, rank_to = int(rank_range[0]), int(rank_range[1])
                            query_filters.append(
                                and_(
                                    Model.latest_ranks.cast(JSON)["corr"]
                                    .as_string()
                                    .cast(Integer)
                                    >= rank_from,
                                    Model.latest_ranks.cast(JSON)["corr"]
                                    .as_string()
                                    .cast(Integer)
                                    <= rank_to,
                                )
                            )
                    except Exception as e:
                        print(e)
                if filter_key == "stake":
                    try:
                        if len(filter_item["in"]) > 0:
                            stake_range = filter_item["in"][0]
                            if isinstance(stake_range, str):
                                stake_range = stake_range.split(",")
                            stake_from, stake_to = (
                                float(stake_range[0]),
                                float(stake_range[1]),
                            )
                            query_filters.append(
                                and_(
                                    Model.nmr_staked >= stake_from - stake_step,
                                    Model.nmr_staked <= stake_to + stake_step,
                                )
                            )
                    except Exception as e:
                        print(e)
                if filter_key == "return3m":
                    try:
                        if len(filter_item["in"]) > 0:
                            return3m_range = filter_item["in"][0]
                            if isinstance(return3m_range, str):
                                return3m_range = return3m_range.split(",")
                            return3m_from, return3m_to = (
                                float(return3m_range[0]),
                                float(return3m_range[1]),
                            )
                            query_filters.append(
                                and_(
                                    Model.latest_returns.cast(JSON)["threeMonths"]
                                    .as_string()
                                    .cast(Float)
                                    >= return3m_from - return3m_step,
                                    Model.latest_returns.cast(JSON)["threeMonths"]
                                    .as_string()
                                    .cast(Float)
                                    <= return3m_to + return3m_step,
                                )
                            )
                    except Exception as e:
                        print(e)

        query = db.query(self.model).join(self.model.model, isouter=True)
        if len(query_filters) > 0:
            query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
            query = query.filter(query_filter)
        count = query.count()
        query = query.order_by(nulls_last(parse_sort_option(sort)))
        data = query.offset(skip).limit(limit).all()

        agg_query = (
            db.query(
                func.min(
                    Model.latest_ranks.cast(JSON)["corr"].as_string().cast(Integer)
                ).label("min_rank"),
                func.max(
                    Model.latest_ranks.cast(JSON)["corr"].as_string().cast(Integer)
                ).label("max_rank"),
                func.min(Model.nmr_staked).label("min_stake"),
                func.max(Model.nmr_staked).label("max_stake"),
                func.min(
                    Model.latest_returns.cast(JSON)["threeMonths"]
                    .as_string()
                    .cast(Float)
                ).label("min_return3m"),
                func.max(
                    Model.latest_returns.cast(JSON)["threeMonths"]
                    .as_string()
                    .cast(Float)
                ).label("max_return3m"),
            )
            .select_from(self.model)
            .join(self.model.model, isouter=True)
        )

        agg_filters = []
        if category_id is not None:
            agg_filters.append(Product.category_id.in_(all_child_category_ids))
        if len(agg_filters) > 0:
            agg_filter = functools.reduce(lambda a, b: and_(a, b), agg_filters)
            agg_query = agg_query.filter(agg_filter)
        agg_stats = agg_query.one()

        aggregations = [
            {
                "attribute_code": "rank",
                "count": None,
                "label": "Rank",
                "options": [
                    {"label": "from", "value": agg_stats.min_rank},
                    {"label": "to", "value": agg_stats.max_rank},
                    {"label": "step", "value": 1},
                    {"label": "decimals", "value": 0},
                ],
            },
            {
                "attribute_code": "stake",
                "count": None,
                "label": "NMR Stake",
                "options": [
                    {"label": "from", "value": agg_stats.min_stake},
                    {"label": "to", "value": agg_stats.max_stake},
                    {"label": "step", "value": stake_step},
                    {"label": "decimals", "value": 2},
                ],
            },
            {
                "attribute_code": "return3m",
                "count": None,
                "label": "3M Return",
                "options": [
                    {"label": "from", "value": agg_stats.min_return3m},
                    {"label": "to", "value": agg_stats.max_return3m},
                    {"label": "step", "value": return3m_step},
                    {"label": "decimals", "value": 2},
                ],
            },
        ]
        return {"total": count, "data": data, "aggregations": aggregations}


product = CRUDProduct(Product)
