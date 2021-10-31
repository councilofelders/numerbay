from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate, FavoriteUpdate


class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, FavoriteUpdate]):
    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = None
    ) -> List[Favorite]:
        return (
            db.query(self.model)
            .filter(Favorite.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_product(
        self, db: Session, *, user_id: int, product_id: int
    ) -> Optional[Favorite]:
        return (
            db.query(self.model)
            .filter(and_(Favorite.user_id == user_id, Favorite.product_id == product_id))
            .first()
        )


favorite = CRUDFavorite(Favorite)
