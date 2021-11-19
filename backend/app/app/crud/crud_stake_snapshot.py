from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.stake_snapshot import StakeSnapshot
from app.schemas.stake_snapshot import StakeSnapshotCreate, StakeSnapshotUpdate


class CRUDStakeSnapshot(
    CRUDBase[StakeSnapshot, StakeSnapshotCreate, StakeSnapshotUpdate]
):
    pass
    # def get_multi_by_product(
    #     self, db: Session, *, product_id: int, skip: int = 0, limit: int = None
    # ) -> List[StakeSnapshot]:
    #     return (
    #         db.query(self.model)
    #         .filter(StakeSnapshot.product_id == product_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )


stake_snapshot = CRUDStakeSnapshot(StakeSnapshot)
