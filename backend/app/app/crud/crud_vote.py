import functools
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.vote import Vote
from app.schemas.vote import VoteCreate, VoteUpdate


class CRUDVote(CRUDBase[Vote, VoteCreate, VoteUpdate]):
    def get_multi_by_poll(
        self,
        db: Session,
        *,
        poll_id: str,
        voter_id: str = None,
        skip: int = 0,
        limit: int = None
    ) -> List[Vote]:
        query_filters = [Vote.poll_id == poll_id]
        if voter_id is not None:
            query_filters.append(Vote.voter_id == voter_id)

        query_filter = functools.reduce(and_, query_filters)

        return db.query(self.model).filter(query_filter).offset(skip).limit(limit).all()


vote = CRUDVote(Vote)
