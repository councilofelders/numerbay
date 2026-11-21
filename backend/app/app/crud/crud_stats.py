""" CRUD for stats """
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from numerapi.base_api import API_TOURNAMENT_URL
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models.stats import Stats
from app.schemas.stats import StatsCreate, StatsUpdate

TOURNAMENT_NAMES = {8: "numerai", 11: "signals", 12: "crypto"}

# Each order's price is spread evenly over the rounds it covers. ROLLUP adds a
# per-round total row (tournament IS NULL) for the distinct counts, which can't
# be summed across tournaments.
SALES_BY_ROUND_SQL = text(
    """
    SELECT r.round_number, c.tournament,
           SUM(o.price / cardinality(o.rounds)) AS value,
           COUNT(*) AS quantity,
           COUNT(DISTINCT o.buyer_id) AS buyers,
           COUNT(DISTINCT p.owner_id) AS sellers,
           COUNT(DISTINCT o.product_id) AS products
    FROM "order" o
    CROSS JOIN LATERAL unnest(o.rounds) AS r(round_number)
    JOIN product p ON p.id = o.product_id
    JOIN category c ON c.id = p.category_id
    WHERE o.state = 'confirmed' AND c.tournament IN (8, 11, 12)
      AND r.round_number <= :last_round
    GROUP BY r.round_number, ROLLUP (c.tournament)
    """
)

ACTIVE_LISTINGS_SQL = text(
    """
    SELECT c.tournament, COUNT(*) AS products, COUNT(DISTINCT p.owner_id) AS sellers
    FROM product p
    JOIN category c ON c.id = p.category_id
    WHERE p.is_active AND c.tournament IN (8, 11, 12)
    GROUP BY ROLLUP (c.tournament)
    """
)


def fetch_round_open_dates() -> Dict[int, str]:
    """Round number -> open date (UTC); all tournaments share round dates"""
    # Plain requests: numerapi sets no timeout, so a stalled call would hang the job.
    response = requests.post(
        API_TOURNAMENT_URL,
        json={"query": "query { rounds(tournament: 8) { number openTime } }"},
        timeout=30,
    )
    response.raise_for_status()
    rounds = response.json()["data"]["rounds"]
    return {r["number"]: r["openTime"][:10] for r in rounds}


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
        """Rebuild per-round sales stats and upsert today's listings snapshot"""
        # Call Numerai before any query so no transaction is held while waiting.
        open_dates = fetch_round_open_dates()
        # Later rounds have only prepaid orders and no open date yet.
        last_round = crud.globals.get_singleton(db).active_round  # type: ignore
        rows = db.execute(SALES_BY_ROUND_SQL, {"last_round": last_round}).all()
        first_round = min((row.round_number for row in rows), default=last_round)
        rounds = range(first_round, last_round + 1)

        value = {name: [0.0] * len(rounds) for name in TOURNAMENT_NAMES.values()}
        quantity = {name: [0] * len(rounds) for name in TOURNAMENT_NAMES.values()}
        buyers, sellers, products = ([0] * len(rounds) for _ in range(3))
        for row in rows:
            i = row.round_number - first_round
            if row.tournament is None:
                buyers[i], sellers[i], products[i] = (
                    row.buyers,
                    row.sellers,
                    row.products,
                )
            else:
                value[TOURNAMENT_NAMES[row.tournament]][i] = round(float(row.value), 6)
                quantity[TOURNAMENT_NAMES[row.tournament]][i] = row.quantity

        today = datetime.utcnow().date().isoformat()
        snapshot: Dict[str, Any] = {"date": today}
        snapshot.update({name: 0 for name in TOURNAMENT_NAMES.values()})
        for row in db.execute(ACTIVE_LISTINGS_SQL):
            if row.tournament is None:
                snapshot["sellers"] = row.sellers
            else:
                snapshot[TOURNAMENT_NAMES[row.tournament]] = row.products

        instance = self.get_singleton(db)
        previous: List[Dict] = (instance.stats or {}).get("listings", [])  # type: ignore
        stats = {
            "start_round": first_round,
            "dates": [open_dates[r] for r in rounds],
            "value": value,
            "quantity": quantity,
            "buyers": buyers,
            "sellers": sellers,
            "products": products,
            "listings": [s for s in previous if s["date"] != today] + [snapshot],
        }
        return super().update(
            db, db_obj=instance, obj_in={"stats": stats}  # type: ignore
        )


stats = CRUDStats(Stats)  # pylint: disable=redefined-builtin
