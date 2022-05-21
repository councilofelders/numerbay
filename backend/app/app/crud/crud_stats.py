""" CRUD for stats """

from typing import Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Order
from app.models.stats import Stats
from app.schemas.stats import StatsCreate, StatsUpdate


def parse_round_stats(series: List[Dict], fill_value: Union[int, float]) -> List[Dict]:
    transposed = {k: [dic[k] for dic in series] for k in series[0]}
    min_round = transposed["round_tournament"][0]
    max_round = transposed["round_tournament"][-1]
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
        stats["sales_value"] = jsonable_encoder(
            db.query(
                Order.round_order.label("round_tournament"),
                func.sum(Order.price).label("value"),
            )
            .filter(Order.state == "confirmed")
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )
        stats["sales_quantity"] = jsonable_encoder(
            db.query(
                Order.round_order.label("round_tournament"),
                func.sum(Order.quantity).label("value"),
            )
            .filter(Order.state == "confirmed")
            .group_by(Order.round_order)
            .order_by(Order.round_order)
            .all()
        )

        stats["sales_value"] = parse_round_stats(stats["sales_value"], fill_value=0)
        stats["sales_quantity"] = parse_round_stats(
            stats["sales_quantity"], fill_value=0
        )

        return super().update(
            db,
            db_obj=instance,  # type: ignore
            obj_in={
                "stats": stats,
            },
        )


stats = CRUDStats(Stats)  # pylint: disable=redefined-builtin
