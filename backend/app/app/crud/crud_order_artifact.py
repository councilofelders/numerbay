""" CRUD for order artifact """

import functools
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.models.order_artifact import OrderArtifact
from app.schemas.order_artifact import OrderArtifactCreate, OrderArtifactUpdate


class CRUDOrderArtifact(
    CRUDBase[OrderArtifact, OrderArtifactCreate, OrderArtifactUpdate]
):
    """CRUD for order artifact"""

    def get_multi_by_order_round(
        self,
        db: Session,
        *,
        order: models.Order,
        round_tournament: int,
        active_only: Optional[bool] = False
    ) -> List[OrderArtifact]:
        """Get multiple order artifacts by order round"""
        query_filters = [OrderArtifact.order_id == order.id]
        if order.product.category.is_per_round:
            query_filters.append(OrderArtifact.round_tournament == round_tournament)
        if active_only:
            query_filters.append(OrderArtifact.state == "active")
        query_filter = functools.reduce(and_, query_filters)
        return db.query(self.model).filter(query_filter).all()

    def bulk_mark_for_pruning(self, db: Session, current_round: int) -> None:
        """Bulk mark order artifacts for storage pruning"""
        artifacts_to_prune = (
            db.query(self.model)
            .join(models.Order)
            .join(models.Product)
            .join(models.Category)
            .filter(self.model.round_tournament < current_round)
            .filter(models.Category.is_per_round)
            .all()
        )
        for artifact in artifacts_to_prune:
            artifact.state = "marked_for_pruning"

        db.commit()


order_artifact = CRUDOrderArtifact(OrderArtifact)
