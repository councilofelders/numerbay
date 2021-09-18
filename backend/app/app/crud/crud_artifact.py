from typing import List

from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.models.artifact import Artifact
from app.schemas.artifact import ArtifactCreate, ArtifactUpdate


class CRUDArtifact(CRUDBase[Artifact, ArtifactCreate, ArtifactUpdate]):
    def get_multi_by_product_round(
        self, db: Session, *, product: models.Product, round_tournament: int
    ) -> List[Artifact]:
        if product.category.is_per_round:
            return (
                db.query(self.model)
                .filter(Artifact.product_id == product.id)
                .filter(Artifact.round_tournament == round_tournament)
                .all()
            )
        else:
            return db.query(self.model).filter(Artifact.product_id == product.id).all()


artifact = CRUDArtifact(Artifact)
