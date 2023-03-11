""" CRUD for Numerai model """

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
    """CRUD for Numerai model"""

    def get_by_name(
        self, db: Session, *, name: str, tournament: int
    ) -> Optional[Model]:
        """Get Numerai model by name"""
        return (
            db.query(self.model)
            .filter(and_(self.model.name == name, self.model.tournament == tournament))
            .first()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: ModelCreate, owner_id: int
    ) -> Model:
        """Create Numerai model with owner"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = None
    ) -> List[Model]:
        """Get multiple Numerai models by owner"""
        return (
            db.query(self.model)
            .filter(Model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_model_unauthenticated(
        self, db: Session, user_json: Dict
    ) -> Optional[str]:
        """Update Numerai model without auth"""
        numerai_models = self.get_multi_by_owner(db, owner_id=user_json["id"])

        try:
            db_models = {}

            for numerai_model in numerai_models:
                try:
                    model_profile = numerai.get_numerai_model_profile(
                        tournament=int(numerai_model.tournament),  # type: ignore
                        model_name=numerai_model.name,  # type: ignore
                    )
                except TypeError as e:
                    # continue if model does not exist
                    if "NoneType" in str(e):
                        print(f"Skip update for model {numerai_model.name}")
                        continue

                db_models[numerai_model.id] = models.Model(  # type: ignore
                    id=numerai_model.id,
                    name=numerai_model.name,
                    tournament=int(numerai_model.tournament),  # type: ignore
                    owner_id=int(user_json["id"]),
                    stake_info=model_profile.get("stakeInfo", {}),
                    nmr_staked=Decimal(model_profile["stakeValue"])
                    if model_profile.get("stakeValue", None)
                    else 0,
                    start_date=model_profile.get("startDate", None),
                    latest_ranks={
                        score["displayName"]: score["rank"]
                        for score in (model_profile.get("latestUserScores", []) or [])
                    },
                    latest_reps={
                        score["displayName"]: score["reputation"]
                        for score in (model_profile.get("latestUserScores", []) or [])
                    },
                    latest_returns=(model_profile.get("latestReturns", {}) or {}),
                    round_model_performances=[],
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
                                model.name
                                for model in numerai_models
                                if int(model.tournament) == 8  # type: ignore
                            ]
                        ),
                        models.StakeSnapshot.tournament == 8,
                    ),
                    and_(
                        models.StakeSnapshot.name.in_(
                            [
                                model.name
                                for model in numerai_models
                                if int(model.tournament) == 11  # type: ignore
                            ]
                        ),
                        models.StakeSnapshot.tournament == 11,
                    ),
                )
            ).update(
                {
                    models.StakeSnapshot.model_id: select(  # type: ignore
                        models.Model.id  # type: ignore
                    )
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

            print(f"Updated user (no auth): {user_json['username']}")
            return user_json["username"]
        except Exception as e:
            print(
                f"Update model (no auth) failed for user {user_json['username']}: {e}"
            )
            raise e

    def update_model(self, db: Session, user_json: Dict) -> Optional[str]:
        """Update Numerai model"""
        if (
            "numerai_api_key_secret" not in user_json
            or user_json["numerai_api_key_secret"] is None
            or user_json["numerai_api_key_secret"] == ""
        ):
            print(
                f"Update model failed for user {user_json['username']}: No Numerai API key"
            )
            return None
        try:
            numerai_models = numerai.get_numerai_models(
                public_id=user_json.get("numerai_api_key_public_id", None),
                secret_key=user_json.get("numerai_api_key_secret"),  # type: ignore
            )  # type: ignore

            db_models = {}

            for numerai_model in numerai_models:
                model_profile = numerai.get_numerai_model_profile(
                    tournament=int(numerai_model["tournament"]),
                    model_name=numerai_model["name"],
                )

                db_models[numerai_model["id"]] = models.Model(  # type: ignore
                    id=numerai_model["id"],
                    name=numerai_model["name"],
                    tournament=int(numerai_model["tournament"]),
                    owner_id=int(user_json["id"]),
                    stake_info=model_profile.get("stakeInfo", {}),
                    nmr_staked=Decimal(model_profile["stakeValue"])
                    if model_profile.get("stakeValue", None)
                    else 0,
                    start_date=model_profile.get("startDate", None),
                    latest_ranks={
                        score["displayName"]: score["rank"]
                        for score in (model_profile.get("latestUserScores", []) or [])
                    },
                    latest_reps={
                        score["displayName"]: score["reputation"]
                        for score in (model_profile.get("latestUserScores", []) or [])
                    },
                    latest_returns=(model_profile.get("latestReturns", {}) or {}),
                    round_model_performances=[],
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
                    models.StakeSnapshot.model_id: select(  # type: ignore
                        models.Model.id  # type: ignore
                    )
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
            print(f"Update model failed for user {user_json['username']}: {e}")
            raise e
        return None

    def batch_update_models(self, db: Session) -> bool:
        """Batch update Numerai models"""
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
                    for user_model in user_models.get("models", []):
                        db_models[user_model["id"]] = Model(  # type: ignore
                            id=user_model["id"],
                            name=user_model["name"],
                            tournament=int(user_model["tournament"]),
                            owner_id=int(user_models["id"]),
                            stake_info=user_model["model_performance"]
                            .get("modelPerformance", {})
                            .get("stakeInfo", {}),
                            nmr_staked=Decimal(
                                user_model["model_performance"]["nmrStaked"]
                            )
                            if user_model["model_performance"].get("nmrStaked", None)
                            else 0,
                            start_date=user_model["model_performance"].get(
                                "startDate", None
                            ),
                            latest_ranks=user_model["model_performance"]
                            .get("modelPerformance", {})
                            .get("latestRanks", {}),
                            latest_reps=user_model["model_performance"]
                            .get("modelPerformance", {})
                            .get("latestReps", {}),
                            latest_returns=user_model["model_performance"]
                            .get("modelPerformance", {})
                            .get("latestReturns", {}),
                            round_model_performances=user_model["model_performance"]
                            .get("modelPerformance", {})
                            .get("roundModelPerformances", []),
                        )
                except Exception as e:  # pylint: disable=broad-except
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
            return True  # pylint: disable=lost-exception
            # db.close()


model = CRUDModel(Model)
