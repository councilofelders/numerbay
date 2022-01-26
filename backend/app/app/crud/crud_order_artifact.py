from typing import List

from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.models.order_artifact import OrderArtifact
from app.schemas.order_artifact import OrderArtifactCreate, OrderArtifactUpdate


class CRUDOrderArtifact(
    CRUDBase[OrderArtifact, OrderArtifactCreate, OrderArtifactUpdate]
):
    def get_multi_by_order_round(
        self, db: Session, *, order: models.Order, round_tournament: int
    ) -> List[OrderArtifact]:
        if order.product.category.is_per_round:
            return (
                db.query(self.model)
                .filter(OrderArtifact.order_id == order.id)
                .filter(OrderArtifact.round_tournament == round_tournament)
                .filter(OrderArtifact.state == "active")
                .all()
            )
        else:
            return db.query(self.model).filter(OrderArtifact.order_id == order.id).all()

    def bulk_mark_for_pruning(self, db: Session, current_round: int) -> None:
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
