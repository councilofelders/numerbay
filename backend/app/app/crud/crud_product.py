""" CRUD for product """

import functools
from typing import Any, Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, func, nulls_last  # type: ignore
from sqlalchemy.orm import Session
from sqlalchemy.types import JSON, Float, Integer

from app import crud
from app.crud.base import CRUDBase
from app.models import Category
from app.models.model import Model
from app.models.product import Product
from app.models.product_option import ProductOption
from app.schemas.product import ProductCreate, ProductUpdate

_SORT_OPTION_LOOKUP = {
    "latest": desc(Product.id),
    # "price-up": Product.price,
    # "price-down": desc(Product.price),
    "name-up": Product.name,
    "name-down": desc(Product.name),
    # "rank-best": Model.latest_ranks.cast(JSON)["tc"].as_string().cast(Integer),
    # "rank-worst": desc(Model.latest_ranks.cast(JSON)["tc"].as_string().cast(Integer)),
    "return3m-up": Model.latest_returns.cast(JSON)["threeMonths"]
    .as_string()
    .cast(Float),
    "return3m-down": desc(
        Model.latest_returns.cast(JSON)["threeMonths"].as_string().cast(Float)
    ),
    "corr-up": Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float),
    "corr-down": desc(Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)),
    "mmc-up": Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float),
    "mmc-down": desc(Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float)),
    "corrmmc-up": Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
    + Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float),
    "corrmmc-down": desc(
        Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
        + Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float)
    ),
    "corr2mmc-up": Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
    + 2.0 * Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float),
    "corr2mmc-down": desc(
        Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
        + 2.0 * Model.latest_reps.cast(JSON)["mmc"].as_string().cast(Float)
    ),
    "corrtc-up": Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
    + Model.latest_reps.cast(JSON)["tc"].as_string().cast(Float),
    "corrtc-down": desc(
        Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
        + Model.latest_reps.cast(JSON)["tc"].as_string().cast(Float)
    ),
    "corr2tc-up": Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
    + 2.0 * Model.latest_reps.cast(JSON)["tc"].as_string().cast(Float),
    "corr2tc-down": desc(
        Model.latest_reps.cast(JSON)["corr"].as_string().cast(Float)
        + 2.0 * Model.latest_reps.cast(JSON)["tc"].as_string().cast(Float)
    ),
    "fnc-up": Model.latest_reps.cast(JSON)["fnc"].as_string().cast(Float),
    "fnc-down": desc(Model.latest_reps.cast(JSON)["fnc"].as_string().cast(Float)),
    "fncV3-up": Model.latest_reps.cast(JSON)["fncV3"].as_string().cast(Float),
    "fncV3-down": desc(Model.latest_reps.cast(JSON)["fncV3"].as_string().cast(Float)),
    "tc-up": Model.latest_reps.cast(JSON)["tc"].as_string().cast(Float),
    "tc-down": desc(Model.latest_reps.cast(JSON)["tc"].as_string().cast(Float)),
    "ic-up": Model.latest_reps.cast(JSON)["ic"].as_string().cast(Float),
    "ic-down": desc(Model.latest_reps.cast(JSON)["ic"].as_string().cast(Float)),
    "stake-up": Model.nmr_staked,
    "stake-down": desc(Model.nmr_staked),
}


def parse_sort_option(sort: Optional[str], category: Optional[Category] = None) -> Any:
    """ Parse sort option """
    if category is not None and category.tournament:
        if category.tournament == 8:
            default_option = (
                Model.latest_ranks.cast(JSON)["tc"].as_string().cast(Integer)
            )
        else:
            default_option = (
                Model.latest_ranks.cast(JSON)["corr"].as_string().cast(Integer)
            )
    else:
        default_option = desc(Product.id)

    if sort:
        return _SORT_OPTION_LOOKUP.get(sort, default_option)
    return default_option


def parse_platform_filter(filter_item: Dict) -> Any:
    """ Parse platform filter """
    with_on_platform = "on-platform" in filter_item["in"]
    with_off_platform = "off-platform" in filter_item["in"]
    platform_list = []
    if with_on_platform:
        platform_list.append(True)
    if with_off_platform:
        platform_list.append(False)
    if len(platform_list) == 0:
        platform_list = [True, False]
    return Product.options.any(ProductOption.is_on_platform.in_(platform_list))


def parse_status_filter(filter_item: Dict) -> Any:
    """ Parse status filter """
    with_active = "active" in filter_item["in"]
    with_inactive = "inactive" in filter_item["in"]
    status_list = []
    if with_active:
        status_list.append(True)
    if with_inactive:
        status_list.append(False)
    if len(status_list) == 0:
        status_list = [True, False]
    return Product.is_active.in_(status_list)


def parse_rank_filter(filter_item: Dict) -> Optional[Any]:
    """ Parse rank filter """
    try:
        if len(filter_item["in"]) > 0:
            rank_range = filter_item["in"][0]
            if isinstance(rank_range, str):
                rank_range = rank_range.split(",")
            rank_from, rank_to = int(rank_range[0]), int(rank_range[1])
            return and_(
                Model.latest_ranks.cast(JSON)["corr"].as_string().cast(Integer)
                >= rank_from,
                Model.latest_ranks.cast(JSON)["corr"].as_string().cast(Integer)
                <= rank_to,
            )
    except Exception as e:  # pylint: disable=broad-except
        print(e)
    return None


def parse_stake_filter(filter_item: Dict, stake_step: float) -> Optional[Any]:
    """ Parse stake filter """
    try:
        if len(filter_item["in"]) > 0:
            stake_range = filter_item["in"][0]
            if isinstance(stake_range, str):
                stake_range = stake_range.split(",")
            stake_from, stake_to = (
                float(stake_range[0]),
                float(stake_range[1]),
            )
            return and_(
                Model.nmr_staked >= stake_from - stake_step,
                Model.nmr_staked <= stake_to + stake_step,
            )
    except Exception as e:  # pylint: disable=broad-except
        print(e)
    return None


def parse_return3m_filter(
    filter_item: Dict, return3m_step: Union[int, float]
) -> Optional[Any]:
    """ Parse 3M return filter """
    try:
        if len(filter_item["in"]) > 0:
            return3m_range = filter_item["in"][0]
            if isinstance(return3m_range, str):
                return3m_range = return3m_range.split(",")
            return3m_from, return3m_to = (
                float(return3m_range[0]),
                float(return3m_range[1]),
            )
            return and_(
                Model.latest_returns.cast(JSON)["threeMonths"].as_string().cast(Float)
                >= return3m_from - return3m_step,
                Model.latest_returns.cast(JSON)["threeMonths"].as_string().cast(Float)
                <= return3m_to + return3m_step,
            )

    except Exception as e:  # pylint: disable=broad-except
        print(e)
    return None


def parse_filters(
    filters: Optional[Dict] = None,
    query_filters: Optional[List] = None,
    stake_step: Union[int, float] = 1,
    return3m_step: float = 0.01,
) -> List:
    """ Parse filters """
    if not isinstance(query_filters, list):
        query_filters = []

    if not isinstance(filters, dict):
        return query_filters

    for filter_key, filter_item in filters.items():
        if filter_key == "id":
            id_list = [int(i) for i in filter_item["in"]]
            query_filters.append(Product.id.in_(id_list))
        if filter_key == "platform":
            query_filters.append(parse_platform_filter(filter_item))
        if filter_key == "status":
            query_filters.append(parse_status_filter(filter_item))
        if filter_key == "user":
            user_id_list = [int(i) for i in filter_item["in"]]
            query_filters.append(Product.owner_id.in_(user_id_list))
        if filter_key == "rank":
            query_filters.append(parse_rank_filter(filter_item))
        if filter_key == "stake":
            query_filters.append(parse_stake_filter(filter_item, stake_step))
        if filter_key == "return3m":
            query_filters.append(parse_return3m_filter(filter_item, return3m_step))

    return query_filters


def generate_aggregations(
    agg_stats: Any, return3m_step: Union[int, float], stake_step: float
) -> List:
    """ Generate aggregations """
    aggregations = [
        {
            "attribute_code": "status",
            "count": None,
            "label": "Status",
            "options": [
                {"label": "active", "value": True},
                {"label": "inactive", "value": False},
            ],
        },
        {
            "attribute_code": "platform",
            "count": None,
            "label": "Platform",
            "options": [
                {"label": "on-platform", "value": True},
                {"label": "off-platform", "value": False},
            ],
        },
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
    return aggregations


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """ CRUD for product """

    def create_with_owner(
        self,
        db: Session,
        *,
        obj_in: ProductCreate,
        owner_id: int,
        sku: str,
        model_id: Optional[str] = None,
        tournament: Optional[int] = 8,
    ) -> Product:
        """ Create product with owner """
        obj_in_data = jsonable_encoder(obj_in)

        if model_id is None:
            if tournament:
                model = crud.model.get_by_name(
                    db, name=obj_in.name, tournament=tournament
                )
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
        """ Get product by sku """
        return db.query(self.model).filter(Product.sku == sku).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = None
    ) -> List[Product]:
        """ Get multiple products by owner """
        return (
            db.query(self.model)
            .filter(Product.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_category(
        self, db: Session, *, category_id: int, skip: int = 0, limit: int = None
    ) -> List[Product]:
        """ Get multiple products by category """
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
        """ Bulk expire products """
        products_to_expire = (
            db.query(self.model).filter(Product.expiration_round < current_round).all()
        )
        for product_obj in products_to_expire:
            product_obj.is_active = False

        db.commit()

    def bulk_unmark_is_ready(self, db: Session) -> None:
        """ Bulk unmark product readiness flag"""
        products_to_unmark = db.query(self.model).filter(Product.is_ready).all()
        for product_obj in products_to_unmark:
            if product_obj.category.is_per_round:
                product_obj.is_ready = False

        db.commit()

    def search(  # pylint: disable=too-many-locals
        self,
        db: Session,
        *,
        id: int = None,  # pylint: disable=W0622
        category_id: int = None,
        skip: int = 0,
        limit: int = None,
        filters: Dict = None,
        term: str = None,
        name: str = None,
        category_slug: str = None,
        sort: str = None,
    ) -> Any:
        """ Search products """
        all_child_categories = crud.category.get_all_subcategories(
            db, category_id=category_id  # type: ignore
        )
        all_child_category_ids = [c[0] for c in all_child_categories]

        query_filters = []
        if id is not None:
            query_filters.append(Product.id == id)
        if category_id is not None:
            query_filters.append(Product.category_id.in_(all_child_category_ids))
        if term is not None:
            query_filters.append(
                Product.name.ilike(
                    "%{}%".format(term)  # pylint: disable=consider-using-f-string
                )
            )
        if name is not None:
            query_filters.append(Product.name == name)
        if category_slug is not None:
            query_filters.append(Category.slug == category_slug)

        stake_step = 1
        return3m_step = 0.01

        query_filters = parse_filters(
            filters=filters,
            query_filters=query_filters,
            stake_step=stake_step,
            return3m_step=return3m_step,
        )

        query = (
            db.query(self.model)
            .join(self.model.category)
            .join(self.model.model, isouter=True)
        )
        if len(query_filters) > 0:
            query_filter = functools.reduce(and_, query_filters)
            query = query.filter(query_filter)
        count = query.count()
        query = query.order_by(
            nulls_last(
                parse_sort_option(
                    sort, all_child_categories[0] if all_child_categories else None
                )
            )
        )
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
            agg_filter = functools.reduce(and_, agg_filters)
            agg_query = agg_query.filter(agg_filter)
        agg_stats = agg_query.one()

        aggregations = generate_aggregations(agg_stats, return3m_step, stake_step)
        return {"total": count, "data": data, "aggregations": aggregations}


product = CRUDProduct(Product)
