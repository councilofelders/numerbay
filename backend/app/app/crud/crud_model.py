import asyncio
import sys
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app import crud, models
from app.api.dependencies import numerai
from app.crud.base import CRUDBase
from app.models.model import Model
from app.schemas.model import ModelCreate, ModelUpdate


class CRUDModel(CRUDBase[Model, ModelCreate, ModelUpdate]):
    def get_by_name(
        self, db: Session, *, name: str, tournament: int
    ) -> Optional[Model]:
        return (
            db.query(self.model)
            .filter(and_(self.model.name == name, self.model.tournament == tournament))
            .first()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: ModelCreate, owner_id: int
    ) -> Model:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = None
    ) -> List[Model]:
        return (
            db.query(self.model)
            .filter(Model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_model(self, db: Session, user_json: Dict) -> Optional[str]:
        if (
            "numerai_api_key_secret" not in user_json
            or user_json["numerai_api_key_secret"] is None
            or user_json["numerai_api_key_secret"] == ""
        ):
            print(f"Update failed user (API Key): {user_json['username']}")
            return None
        try:
            numerai_models = numerai.get_numerai_models(
                public_id=user_json.get("numerai_api_key_public_id", None),
                secret_key=user_json.get("numerai_api_key_secret"),  # type: ignore
            )  # type: ignore

            db_models = {}

            for model in numerai_models:
                model_performance = numerai.get_numerai_model_performance(
                    tournament=int(model["tournament"]), model_name=model["name"]
                )
                model["model_performance"] = model_performance

                db_models[model["id"]] = models.Model(  # type: ignore
                    id=model["id"],
                    name=model["name"],
                    tournament=int(model["tournament"]),
                    owner_id=int(user_json["id"]),
                    nmr_staked=Decimal(model["model_performance"]["nmrStaked"])
                    if model["model_performance"].get("nmrStaked", None)
                    else 0,
                    start_date=model["model_performance"].get("startDate", None),
                    latest_ranks=model["model_performance"]
                    .get("modelPerformance", {})
                    .get("latestRanks", {}),
                    latest_reps=model["model_performance"]
                    .get("modelPerformance", {})
                    .get("latestReps", {}),
                    latest_returns=model["model_performance"]
                    .get("modelPerformance", {})
                    .get("latestReturns", {}),
                    round_model_performances=model["model_performance"]
                    .get("modelPerformance", {})
                    .get("roundModelPerformances", []),
                )

            for db_model in (
                db.query(models.Model)
                .filter(models.Model.id.in_(db_models.keys()))
                .all()
            ):
                # Updates
                db.merge(db_models.pop(db_model.id))

            # Inserts
            db.add_all(db_models.values())
            db.commit()

            # Connect stake snapshots
            db.query(models.StakeSnapshot).filter(
                or_(
                    and_(
                        models.StakeSnapshot.name.in_(
                            [
                                model["name"]
                                for model in numerai_models
                                if int(model["tournament"]) == 8
                            ]
                        ),
                        models.StakeSnapshot.tournament == 8,
                    ),
                    and_(
                        models.StakeSnapshot.name.in_(
                            [
                                model["name"]
                                for model in numerai_models
                                if int(model["tournament"]) == 11
                            ]
                        ),
                        models.StakeSnapshot.tournament == 11,
                    ),
                )
            ).update(
                {
                    models.StakeSnapshot.model_id: select(models.Model.id)  # type: ignore
                    .where(
                        and_(
                            models.Model.name == models.StakeSnapshot.name,
                            models.Model.tournament == models.StakeSnapshot.tournament,
                        )
                    )
                    .scalar_subquery()
                },
                synchronize_session=False,
            )
            db.commit()

            print(f"Updated user: {user_json['username']}")
            return user_json["username"]
        except ValueError as e:
            if "invalid or has expired" in str(e):  # invalid API keys
                print(f"Invalid API key for user {user_json['username']}: {e}")
                return None
        except Exception as e:
            print(f"Update failed user (Exception): {user_json['username']}: {e}")
            raise e
        return None

    def batch_update_models(self, db: Session) -> bool:
        try:
            print(f"{datetime.utcnow()} Running batch_update_models...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            users = crud.user.search(
                db, filters={"numerai_api_key_public_id": ["any"]}
            )["data"]
            tasks = []
            for user in users:
                tasks.append(numerai.fetch_single_user_models(user=user))
            all_user_models = loop.run_until_complete(
                asyncio.gather(*tasks, return_exceptions=True)
            )

            # ingest numerai models to db
            db_models = {}
            for user_models in all_user_models:
                try:
                    for model in user_models.get("models", []):
                        db_models[model["id"]] = Model(  # type: ignore
                            id=model["id"],
                            name=model["name"],
                            tournament=int(model["tournament"]),
                            owner_id=int(user_models["id"]),
                            nmr_staked=Decimal(model["model_performance"]["nmrStaked"])
                            if model["model_performance"].get("nmrStaked", None)
                            else 0,
                            start_date=model["model_performance"].get(
                                "startDate", None
                            ),
                            latest_ranks=model["model_performance"]
                            .get("modelPerformance", {})
                            .get("latestRanks", {}),
                            latest_reps=model["model_performance"]
                            .get("modelPerformance", {})
                            .get("latestReps", {}),
                            latest_returns=model["model_performance"]
                            .get("modelPerformance", {})
                            .get("latestReturns", {}),
                            round_model_performances=model["model_performance"]
                            .get("modelPerformance", {})
                            .get("roundModelPerformances", []),
                        )
                except Exception as e:
                    print(e)
                continue

            for db_model in (
                db.query(Model).filter(Model.id.in_(db_models.keys())).all()
            ):
                # Updates
                db.merge(db_models.pop(db_model.id))

            # Inserts
            db.add_all(db_models.values())
            db.commit()

            print(f"{datetime.utcnow()} Finished batch_update_models")
        finally:
            sys.stdout.flush()
            return True
            # db.close()


model = CRUDModel(Model)
