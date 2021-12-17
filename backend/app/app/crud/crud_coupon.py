import functools
from typing import Optional

from sqlalchemy import and_, func  # type: ignore
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate, CouponUpdate


class CRUDCoupon(CRUDBase[Coupon, CouponCreate, CouponUpdate]):
    def get_by_code(
        self, db: Session, *, code: Optional[str] = None
    ) -> Optional[Coupon]:
        if not code:
            return None
        query_filters = [
            func.upper(self.model.code) == func.upper(code),
            self.model.state.is_(None),
        ]
        query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
        return db.query(self.model).filter(query_filter).first()


coupon = CRUDCoupon(Coupon)
