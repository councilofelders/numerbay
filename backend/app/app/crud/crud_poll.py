import functools
from typing import Any, Dict, Optional

from sqlalchemy import and_, desc, nulls_last  # type: ignore
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.poll import Poll
from app.schemas.poll import PollCreate, PollUpdate


def parse_sort_option(sort: Optional[str]) -> Any:  # pylint: disable=W0613
    return desc(Poll.id)


class CRUDPoll(CRUDBase[Poll, PollCreate, PollUpdate]):
    def search(
        self,
        db: Session,
        *,
        id: str = None,  # pylint: disable=W0622
        skip: int = 0,
        limit: int = None,
        filters: Dict = None,
        term: str = None,  # pylint: disable=W0613
        sort: str = None,
    ) -> Any:
        query_filters = []
        if id is not None:
            query_filters.append(Poll.id == id)
        # if term is not None:
        #     query_filters.append(Product.name.ilike("%{}%".format(term)))

        if isinstance(filters, dict):
            for filter_key, filter_item in filters.items():
                if filter_key == "user":
                    user_id_list = [int(i) for i in filter_item["in"]]
                    query_filters.append(Poll.owner_id.in_(user_id_list))

        query = db.query(self.model)
        if len(query_filters) > 0:
            query_filter = functools.reduce(and_, query_filters)
            query = query.filter(query_filter)
        count = query.count()
        query = query.order_by(nulls_last(parse_sort_option(sort)))
        data = query.offset(skip).limit(limit).all()

        return {"total": count, "data": data}


poll = CRUDPoll(Poll)
