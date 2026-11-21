from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.crud import crud_stats
from app.schemas import CategoryCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def _at(stats, series, round_number):
    i = round_number - stats["start_round"]
    return series[i] if 0 <= i < len(series) else 0


def _today_snapshots(stats):
    today = datetime.utcnow().date().isoformat()
    return [s for s in stats["listings"] if s["date"] == today]


def test_update_stats(db: Session, monkeypatch) -> None:
    monkeypatch.setattr(
        crud_stats, "fetch_round_open_dates", lambda: {r: f"d{r}" for r in range(5000)}
    )
    last = crud.globals.get_singleton(db).active_round  # type: ignore
    original = crud.stats.get_singleton(db).stats  # type: ignore
    crud.stats.update(
        db,
        db_obj=crud.stats.get_singleton(db),  # type: ignore
        obj_in={"stats": {"listings": [{"date": "2000-01-01", "sellers": 1}]}},
    )
    before = crud.stats.update_stats(db).stats

    created: list = []

    def add(obj):
        db.add(obj)
        db.commit()
        created.append(obj)
        return obj

    def category(tournament):
        name = random_lower_string()
        obj = crud.category.create(
            db, obj_in=CategoryCreate(name=name, slug=name, tournament=tournament)
        )
        created.append(obj)
        return obj

    def product(cat, owner):
        name = random_lower_string()
        return add(
            models.Product(
                name=name, sku=f"stats-{name}", category_id=cat.id, owner_id=owner.id
            )
        )

    def order(prod, buyer, rounds, price, state="confirmed"):
        return add(
            models.Order(
                date_order=datetime.utcnow(),
                round_order=rounds[0],
                rounds=rounds,
                price=Decimal(price),
                currency="NMR",
                product_id=prod.id,
                buyer_id=buyer.id,
                state=state,
            )
        )

    seller_a, seller_b, buyer_x, buyer_y = (create_random_user(db) for _ in range(4))
    created.extend([seller_a, seller_b, buyer_x, buyer_y])
    try:
        crypto = product(category(12), seller_a)
        numerai = product(category(8), seller_b)
        merch = product(category(None), seller_a)
        order(crypto, buyer_x, [last - 1, last, last + 5], 3)  # 1 NMR per round
        order(crypto, buyer_y, [last], 2)
        order(numerai, buyer_x, [last], 1)
        order(merch, buyer_x, [last], 10)  # not a tournament product
        order(numerai, buyer_y, [last], 5, state="pending")

        after = crud.stats.update_stats(db).stats

        def delta(path, round_number=last):
            def at(stats):
                series = stats
                for key in path.split("."):
                    series = series[key]
                return _at(stats, series, round_number)

            return at(after) - at(before)

        assert delta("value.crypto") == pytest.approx(3.0)
        assert delta("value.crypto", last - 1) == pytest.approx(1.0)
        assert delta("quantity.crypto") == 2
        assert delta("value.numerai") == pytest.approx(1.0)
        assert delta("quantity.numerai") == 1
        assert delta("value.signals") == pytest.approx(0)
        assert delta("buyers") == 2
        assert delta("sellers") == 2
        assert delta("products") == 2
        # Prepaid future rounds are left out; every round has an open date.
        assert after["dates"][-1] == f"d{last}"
        assert len(after["dates"]) == last - after["start_round"] + 1

        assert {"date": "2000-01-01", "sellers": 1} in after["listings"]
        [snap_before] = _today_snapshots(before)
        [snap_after] = _today_snapshots(after)
        assert snap_after["crypto"] - snap_before["crypto"] == 1
        assert snap_after["numerai"] - snap_before["numerai"] == 1
        assert snap_after["sellers"] - snap_before["sellers"] == 2
    finally:
        for obj in reversed(created):
            db.delete(obj)
        db.commit()
        crud.stats.update(
            db,
            db_obj=crud.stats.get_singleton(db),  # type: ignore
            obj_in={"stats": original},
        )
