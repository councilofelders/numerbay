""" CRUD for stats """
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from numerapi import NumerAPI
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models import Artifact, Category, Model, Order, Product
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


def get_last_artifact_for_order(db: Session, order_json: Dict) -> Optional[Dict]:
    if order_json["buyer_public_key"] is not None:  # uses encryption
        last_artifact = None
        for artifact in order_json.get("artifacts", []):
            if artifact["round_tournament"] == order_json["round_order"]:
                last_artifact = artifact
        return last_artifact
    else:
        artifacts = (
            db.query(Artifact)
            .filter(
                Artifact.product_id == order_json["product_id"],
                Artifact.round_tournament == order_json["round_order"],
            )
            .all()
        )
        if isinstance(artifacts, list) and len(artifacts) > 0:
            return jsonable_encoder(artifacts[-1])
        return None


def get_stake_for_model_round(
    db: Session, model_id: str, round_tournament: int
) -> Decimal:
    round_model_performances = (
        db.query(Model.round_model_performances).filter(Model.id == model_id).first()
    )
    if round_model_performances and len(round_model_performances) > 0:
        round_model_performance = list(
            filter(
                lambda perf: perf.get("roundNumber", None) == round_tournament,
                round_model_performances[0],
            )
        )
        if round_model_performance and len(round_model_performance) > 0:
            stake = Decimal(
                round_model_performance[0].get("selectedStakeValue", "0") or "0"
            )
            return stake
    return Decimal("0")


def get_submissions_for_model(
    public_id: str, secret_key: str, model_id: str, tournament: int
) -> List:
    query = """
        query($modelId: String!) {
          model(modelId: $modelId) {
            signalsSubmissions {
              filename
              insertedAt
            }
            submissions {
              filename
              insertedAt
            }
          }
        }
    """
    api = NumerAPI(public_id=public_id, secret_key=secret_key)
    try:
        data = api.raw_query(query, {"modelId": model_id}, authorization=True)["data"]
        if data is not None and "submissions" in data:
            if tournament == 8:
                return data["submissions"]
            else:
                return data["signalsSubmissions"]
    except ValueError:
        pass
    return []


def has_file(submissions: List, filename: str) -> bool:
    for submission in submissions:
        if submission.get("filename", None) == filename:
            return True
    return False


def get_estimated_stake_for_order(
    db: Session, order_json: Dict, artifact_json: Dict
) -> Decimal:
    user = crud.user.get(db, id=order_json["buyer_id"])
    if (
        user is None or user.models is None or user.numerai_api_key_public_id is None
    ):  # type: ignore
        return Decimal("0")

    for model in user.models:  # type: ignore
        submissions = get_submissions_for_model(
            user.numerai_api_key_public_id,
            user.numerai_api_key_secret,  # type: ignore
            model_id=model.id,
            tournament=model.tournament,
        )
        submitted = has_file(submissions, artifact_json["object_name"])

        if submitted:
            stake = get_stake_for_model_round(
                db, model_id=model.id, round_tournament=order_json["round_order"]
            )
            return stake
    return Decimal("0")


def get_stake_for_order(db: Session, order_json: Dict) -> Decimal:
    artifact_json = get_last_artifact_for_order(db, order_json)
    if artifact_json is None:
        return Decimal("0")

    if order_json.get("submit_model_id", None) is not None:  # auto-submit
        return get_stake_for_model_round(
            db,
            model_id=order_json["submit_model_id"],
            round_tournament=order_json["round_order"],
        )
    else:  # no auto-submit, do fuzzy match
        return get_estimated_stake_for_order(db, order_json, artifact_json)


def calculate_stake_for_tournament(
    db: Session, tournament: int, round_tournament: int
) -> List:
    orders = (
        db.query(Order)
        .join(Order.product, Product.category)
        .filter(
            Order.state == "confirmed",
            Category.tournament == tournament,
            Category.is_submission.is_(True),
        )
        .all()
    )
    flattened_orders = []

    # gather flattened round-orders
    for order in orders:
        order_json = jsonable_encoder(order)
        order_json["artifacts"] = jsonable_encoder(order.artifacts)
        order_json["product"].pop("category", None)
        order_json["product"].pop("description", None)
        order_json["product"].pop("featured_products", None)

        if order.quantity == 1:
            flattened_orders.append(order_json)
        else:
            for i in range(order.quantity):
                order_json_i = order_json.copy()
                order_json_i["round_order"] += i

    # filter flatten orders by tournament round
    flattened_orders = filter(
        lambda flattened_order: flattened_order.get("round_order", None) == round_tournament,
        flattened_orders
    )

    round_stakes = {}
    for order_json in flattened_orders:
        stake = get_stake_for_order(db, order_json)
        if order_json["round_order"] not in round_stakes:
            round_stakes[order_json["round_order"]] = Decimal("0")
        round_stakes[order_json["round_order"]] += stake
    round_stakes_list = [
        {"round_tournament": round_tournament, "value": float(stake)}
        for round_tournament, stake in round_stakes.items()
    ]
    return round_stakes_list


def fill_round_stats(
    existing_data_dict: Dict,
    db: Session,
    function: Callable,
    min_round: int,
    max_round: int,
    **kwargs: Any,
) -> List:
    for round_tournament in range(min_round, max_round + 1):
        print(
            f"Filling stats for round {round_tournament} / [{min_round},  {max_round}]"
        )
        round_stats = function(db, **kwargs, round_tournament=round_tournament)
        if round_stats:
            existing_data_dict[round_tournament] = round_stats[0]["value"]
        else:
            existing_data_dict[round_tournament] = 0
    return [
        {"round_tournament": round_tournament, "value": value}
        for round_tournament, value in existing_data_dict.items()
    ]


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

        # Sales value
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

        # # Sales quantity
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

        # Unique buyers
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

        # Unique models
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

        # Estimated stake
        current_round = crud.globals.get_singleton(db).selling_round  # type: ignore
        stats["estimated_stake_numerai"] = fill_round_stats(
            {
                d["round_tournament"]: d["value"]
                for d in stats.get("estimated_stake_numerai", [])
            },
            db,
            calculate_stake_for_tournament,
            min_round=current_round - 1,
            max_round=current_round,
            tournament=8,
        )
        stats["estimated_stake_signals"] = fill_round_stats(
            {
                d["round_tournament"]: d["value"]
                for d in stats.get("estimated_stake_signals", [])
            },
            db,
            calculate_stake_for_tournament,
            min_round=current_round - 1,
            max_round=current_round,
            tournament=11,
        )

        stats = {
            k: parse_round_stats(
                v, fill_value=0, min_round=min_round, max_round=max_round
            )
            for k, v in stats.items()
        }

        stats["estimated_stake"] = [
            {
                "round_tournament": stats["estimated_stake_numerai"][i][
                    "round_tournament"
                ],
                "value": stats["estimated_stake_numerai"][i]["value"]
                + stats["estimated_stake_signals"][i]["value"],
            }
            for i in range(len(stats["estimated_stake_numerai"]))
        ]

        return super().update(
            db,
            db_obj=instance,  # type: ignore
            obj_in={
                "stats": stats,
            },
        )


stats = CRUDStats(Stats)  # pylint: disable=redefined-builtin
