from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.artifact import Artifact
from app.schemas.artifact import ArtifactCreate, ArtifactUpdate


class CRUDArtifact(CRUDBase[Artifact, ArtifactCreate, ArtifactUpdate]):
    def get_multi_by_product_round(
        self, db: Session, *, product_id: int, round_tournament: int = None
    ) -> List[Artifact]:
        return (
            db.query(self.model)
            .filter(Artifact.product_id == product_id)
            .filter((Artifact.round_tournament == round_tournament) if round_tournament else None)
            .all()
        )


artifact = CRUDArtifact(Artifact)
