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
                .all()
            )
        else:
            return db.query(self.model).filter(OrderArtifact.order_id == order.id).all()


order_artifact = CRUDOrderArtifact(OrderArtifact)
