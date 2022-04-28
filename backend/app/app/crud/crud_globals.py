""" CRUD for globals """

from datetime import datetime, timezone
from typing import Dict, Optional

import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.api.dependencies import numerai
from app.crud.base import CRUDBase
from app.models.globals import Globals
from app.schemas.globals import GlobalsCreate, GlobalsUpdate


class CRUDGlobals(CRUDBase[Globals, GlobalsCreate, GlobalsUpdate]):
    """ CRUD for globals """

    def get_selling_round(self, active_round: Dict) -> int:
        """ Get selling round """
        utc_time = datetime.now(timezone.utc)
        open_time = pd.to_datetime(active_round["openTime"]).to_pydatetime()
        close_staking_time = pd.to_datetime(
            active_round["closeStakingTime"]
        ).to_pydatetime()
        if (  # pylint: disable=no-else-return
            utc_time > close_staking_time
        ):  # previous round closed for staking, next round not yet opened
            return active_round["number"] + 1
        elif utc_time >= open_time:  # new round opened and active
            return active_round["number"]
        # should not happen
        return active_round["number"]

    def get_singleton(self, db: Session) -> Optional[Globals]:
        """ Get globals singleton """
        instance = db.query(self.model).filter(self.model.id == 0).one_or_none()
        if instance:
            return instance
        active_round = numerai.get_numerai_active_round()
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
        """ Update globals singleton """
        instance = self.get_singleton(db)
        active_round = numerai.get_numerai_active_round()
        selling_round_number = self.get_selling_round(active_round)
        return super().update(
            db,
            db_obj=instance,  # type: ignore
            obj_in={
                "active_round": active_round["number"],
                "selling_round": selling_round_number,
            },
        )

    def update_stats(self, db: Session) -> Globals:
        """ Update global stats """
        instance = self.get_singleton(db)
        total_num_products = (
            db.query(func.count(models.Product.id))
            .filter(models.Product.is_active)
            .scalar()
        )
        total_num_sales = (
            db.query(func.count(models.Order.id))
            .filter(models.Order.state == "confirmed")
            .scalar()
        )
        total_qty_sales = (
            db.query(func.sum(models.Order.quantity))
            .filter(models.Order.state == "confirmed")
            .scalar()
        )
        total_sales_nmr = (
            db.query(func.sum(models.Order.price))
            .filter(models.Order.state == "confirmed")
            .scalar()
        )
        return super().update(
            db,
            db_obj=instance,  # type: ignore
            obj_in={
                "total_num_products": total_num_products,
                "total_num_sales": total_num_sales,
                "total_qty_sales": total_qty_sales,
                "total_sales_nmr": total_sales_nmr,
            },
        )


globals = CRUDGlobals(Globals)  # pylint: disable=redefined-builtin
