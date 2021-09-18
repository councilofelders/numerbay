from datetime import datetime, timezone
from typing import Dict, Optional

import pandas as pd
from numerapi import NumerAPI
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.globals import Globals
from app.schemas.globals import GlobalsCreate, GlobalsUpdate


class CRUDGlobals(CRUDBase[Globals, GlobalsCreate, GlobalsUpdate]):
    def get_numerai_active_round(self) -> Dict:
        """
        Retrieve products.
        """
        query = """
                  query {
                    rounds(tournament: 8
                           number: 0) {
                      number
                      openTime
                      closeTime
                      closeStakingTime
                    }
                  }
                """

        api = NumerAPI()
        active_round = api.raw_query(query)["data"]["rounds"][0]
        return active_round

    def get_selling_round(self, active_round: Dict) -> int:
        utc_time = datetime.now(timezone.utc)
        open_time = pd.to_datetime(active_round["openTime"]).to_pydatetime()
        close_staking_time = pd.to_datetime(
            active_round["closeStakingTime"]
        ).to_pydatetime()
        if (
            utc_time > close_staking_time
        ):  # previous round closed for staking, next round not yet opened
            return active_round["number"] + 1
        elif utc_time >= open_time:  # new round opened and active
            return active_round["number"]
        else:  # should not happen
            return active_round["number"]

    def get_singleton(self, db: Session) -> Optional[Globals]:
        instance = db.query(self.model).filter(self.model.id == 0).one_or_none()
        if instance:
            return instance
        else:
            active_round = self.get_numerai_active_round()
            selling_round_number = self.get_selling_round(active_round)
            instance = Globals(
                id=0,
                **{
                    "active_round": active_round["number"],
                    "selling_round": selling_round_number,
                }
            )
            db.add(instance)
            db.commit()
            db.refresh(instance)
            return instance

    def update_singleton(self, db: Session) -> Globals:
        instance = self.get_singleton(db)
        active_round = self.get_numerai_active_round()
        selling_round_number = self.get_selling_round(active_round)
        return super().update(
            db,
            db_obj=instance,  # type: ignore
            obj_in={
                "active_round": active_round["number"],
                "selling_round": selling_round_number,
            },
        )


globals = CRUDGlobals(Globals)
