import asyncio
import sys
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from numerapi import NumerAPI
from sqlalchemy.orm import Session

from app import crud, models
from app.crud.base import CRUDBase
from app.models.model import Model
from app.schemas import User
from app.schemas.model import ModelCreate, ModelUpdate


async def fetch_single_user_models(user: User) -> Dict:
    from app.api.api_v1.endpoints.numerai import (
        get_numerai_models,
        get_numerai_model_performance,
    )

    models = get_numerai_models(current_user=user)  # type: ignore
    for model in models:
        model_performance = get_numerai_model_performance(
            tournament=int(model["tournament"]), model_name=model["name"]
        )
        model["model_performance"] = model_performance
    return {"id": user.id, "models": models}


def normalize_data(data: Dict, tournament: int = 8) -> Dict:
    normalized_data = {"rounds": data["rounds"]}
    normalized_data["modelPerformance"] = {}
    if tournament == 8:
        normalized_data["modelPerformance"] = data["v3UserProfile"]
        normalized_data["nmrStaked"] = data["v3UserProfile"]["nmrStaked"]
        normalized_data["startDate"] = data["v3UserProfile"]["startDate"]
    else:
        normalized_data["nmrStaked"] = data["v2SignalsProfile"]["nmrStaked"]
        normalized_data["startDate"] = data["v2SignalsProfile"]["startDate"]
        normalized_data["modelPerformance"] = {}
        if data["v2SignalsProfile"]["latestRanks"]:
            normalized_data["modelPerformance"]["latestRanks"] = {
                "corr": data["v2SignalsProfile"]["latestRanks"]["corr"],
                "mmc": data["v2SignalsProfile"]["latestRanks"]["mmc"],
            }
            normalized_data["modelPerformance"]["latestReps"] = {
                "corr": data["v2SignalsProfile"]["latestReps"]["corr"],
                "mmc": data["v2SignalsProfile"]["latestReps"]["mmc"],
            }
            normalized_data["modelPerformance"]["latestReturns"] = data[
                "v2SignalsProfile"
            ]["latestReturns"]
        else:
            normalized_data["modelPerformance"]["latestRanks"] = {}
            normalized_data["modelPerformance"]["latestReps"] = {}
            normalized_data["modelPerformance"]["latestReturns"] = {}
        normalized_data["modelPerformance"]["roundModelPerformances"] = []
        for round_performance in data["v2SignalsProfile"]["roundModelPerformances"]:
            if round_performance["corr"] is not None:
                normalized_data["modelPerformance"]["roundModelPerformances"].append(
                    round_performance
                )
    return normalized_data


class CRUDModel(CRUDBase[Model, ModelCreate, ModelUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Model]:
        return db.query(self.model).filter(self.model.name == name).first()

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
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Model]:
        return (
            db.query(self.model)
            .filter(Model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_numerai_models(self, public_id: str, secret_key: str) -> Any:
        """
        Retrieve products.
        """
        query = """
                  query {
                    account {
                      username
                      email
                      id
                      status
                      insertedAt
                      models {
                        id
                        name
                        tournament
                        profileUrl
                      }
                      apiTokens {
                        name
                        public_id
                        scopes
                      }
                    }
                  }
                """

        api = NumerAPI(public_id=public_id, secret_key=secret_key)
        account = api.raw_query(query, authorization=True)["data"]["account"]
        all_models = account["models"]
        return all_models

    def get_numerai_model_performance(self, tournament: int, model_name: str) -> Any:
        """
        Retrieve products.
        """
        numerai_query = """
                query($username: String!) {
                  rounds(tournament: 8, number: 0) {
                    number
                  },
                  v3UserProfile(modelName: $username) {
                    startDate
                    nmrStaked
                    roundModelPerformances {
                      roundNumber
                      corr
                      mmc
                    }
                    latestReps {
                      corr
                      mmc
                    }
                    latestRanks {
                      corr
                      mmc
                    }
                    latestReturns {
                      oneDay
                      threeMonths
                      oneYear
                    }
                  }
                }
        """

        signals_query = """
                query($username: String!) {
                  rounds(tournament: 8, number: 0) {
                    number
                  },
                  v2SignalsProfile(modelName: $username) {
                    startDate
                    nmrStaked
                    roundModelPerformances {
                      roundNumber
                      corr
                      mmc
                    }
                    latestReps {
                      corr
                      mmc
                    }
                    latestRanks {
                      corr
                      mmc
                    }
                    latestReturns {
                      oneDay
                      threeMonths
                      oneYear
                    }
                  }
                }
        """

        if tournament == 8:
            query = numerai_query
        elif tournament == 11:
            query = signals_query

        arguments = {"username": model_name}
        api = NumerAPI()
        data = api.raw_query(query, arguments)["data"]
        data = normalize_data(data, tournament=tournament)

        return data

    def update_model(self, db: Session, user_json: Dict) -> Optional[str]:
        if (
            "numerai_api_key_secret" not in user_json
            or user_json["numerai_api_key_secret"] is None
            or user_json["numerai_api_key_secret"] == ""
        ):
            print(f"Update failed user (API Key): {user_json['username']}")
            return None
        try:
            numerai_models = crud.model.get_numerai_models(
                public_id=user_json.get("numerai_api_key_public_id", None),
                secret_key=user_json.get("numerai_api_key_secret"),  # type: ignore
            )  # type: ignore

            db_models = {}

            for model in numerai_models:
                model_performance = crud.model.get_numerai_model_performance(
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

            print(f"Updated user: {user_json['username']}")
            return user_json["username"]
        except Exception as e:
            print(f"Update failed user (Exception): {user_json['username']}: {e}")
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
                tasks.append(fetch_single_user_models(user=user))
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
