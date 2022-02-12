""" CRUD for stake snapshot """

from app.crud.base import CRUDBase
from app.models.stake_snapshot import StakeSnapshot
from app.schemas.stake_snapshot import StakeSnapshotCreate, StakeSnapshotUpdate


class CRUDStakeSnapshot(
    CRUDBase[StakeSnapshot, StakeSnapshotCreate, StakeSnapshotUpdate]
):
    """ CRUD for stake snapshot """


stake_snapshot = CRUDStakeSnapshot(StakeSnapshot)
