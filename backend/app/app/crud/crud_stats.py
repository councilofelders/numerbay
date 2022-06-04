""" CRUD for stats """

from typing import Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Category, Order, Product
from app.models.stats import Stats
from app.schemas.stats import StatsCreate, StatsUpdate


def parse_round_stats(
    series: List[Dict], fill_value: Union[int, float], min_round: int, max_round: int
) -> List[Dict]:
    transposed = {k: [dic[k] for dic in series] for k in series[0]}
    zipped = dict(zip(transposed["round_tournament"], transposed["value"]))
    for round_tournament in range(min_round, max_round + 1):
        if round_tournament not in zipped:
            zipped[round_tournament] = fill_value
    return sorted(
        [{"round_tournament": k, "value": v} for k, v in zipped.items()],
        key=lambda d: d["round_tournament"],
    )


class CRUDStats(CRUDBase[Stats, StatsCreate, StatsUpdate]):
    """CRUD for stats"""

    def get_singleton(self, db: Session) -> Optional[Stats]:
        """Get stats singleton"""
        instance = db.query(self.model).filter(self.model.id == 0).one_or_none()
        if instance:
            return instance
        instance = Stats(id=0)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def update_stats(self, db: Session) -> Stats:
        """Update stats stats"""
        instance = self.get_singleton(db)
        stats = {}

        sales_value_base_query = db.query(
            Order.round_order.label("round_tournament"),
            func.sum(Order.price).label("value"),
        )
        stats["sales_value"] = jsonable_encoder(
            sales_value_base_query.filter(Order.state == "confirmed")
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )
        stats["sales_value_numerai"] = jsonable_encoder(
            sales_value_base_query.join(Order.product, Product.category)
            .filter(Order.state == "confirmed", Category.tournament == 8)
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )
        stats["sales_value_signals"] = jsonable_encoder(
            sales_value_base_query.join(Order.product, Product.category)
            .filter(Order.state == "confirmed", Category.tournament == 11)
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )

        sales_quantity_base_query = db.query(
            Order.round_order.label("round_tournament"),
            func.sum(Order.quantity).label("value"),
        )
        stats["sales_quantity"] = jsonable_encoder(
            sales_quantity_base_query.filter(Order.state == "confirmed")
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )
        stats["sales_quantity_numerai"] = jsonable_encoder(
            sales_quantity_base_query.join(Order.product, Product.category)
            .filter(Order.state == "confirmed", Category.tournament == 8)
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )
        stats["sales_quantity_signals"] = jsonable_encoder(
            sales_quantity_base_query.join(Order.product, Product.category)
            .filter(Order.state == "confirmed", Category.tournament == 11)
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )

        stats["unique_buyers"] = jsonable_encoder(
            db.query(
                Order.round_order.label("round_tournament"),
                func.count(distinct(Order.buyer_id)).label("value"),
            )
            .filter(Order.state == "confirmed")
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )

        unique_models_sold_base_query = db.query(
            Order.round_order.label("round_tournament"),
            func.count(distinct(Product.model_id)).label("value"),
        ).join(Order.product, Product.category)
        stats["unique_models_sold"] = jsonable_encoder(
            unique_models_sold_base_query.filter(Order.state == "confirmed")
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )
        stats["unique_models_sold_numerai"] = jsonable_encoder(
            unique_models_sold_base_query.filter(
                Order.state == "confirmed", Category.tournament == 8
            )
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )
        stats["unique_models_sold_signals"] = jsonable_encoder(
            unique_models_sold_base_query.filter(
                Order.state == "confirmed", Category.tournament == 11
            )
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )

        min_round = stats["sales_value"][0]["round_tournament"]
        max_round = stats["sales_value"][-1]["round_tournament"]
        # stats_to_parse = [
        #     "sales_value",
        #     "sales_value_numerai",
        #     "sales_value_signals",
        #     "sales_quantity",
        #     "sales_quantity_numerai",
        #     "sales_quantity_signals",
        #     "unique_models_sold",
        #     "unique_models_sold_numerai",
        #     "unique_models_sold_signals",
        #     "unique_buyers",
        # ]

        stats = {
            k: parse_round_stats(
                v, fill_value=0, min_round=min_round, max_round=max_round
            )
            for k, v in stats.items()
        }

        return super().update(
            db,
            db_obj=instance,  # type: ignore
            obj_in={
                "stats": stats,
            },
        )


stats = CRUDStats(Stats)  # pylint: disable=redefined-builtin
