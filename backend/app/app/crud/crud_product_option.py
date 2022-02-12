""" CRUD for product option """

from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.product_option import ProductOption
from app.schemas.product_option import ProductOptionCreate, ProductOptionUpdate


class CRUDProductOption(
    CRUDBase[ProductOption, ProductOptionCreate, ProductOptionUpdate]
):
    def get_multi_by_product(
        self, db: Session, *, product_id: int, skip: int = 0, limit: int = None
    ) -> List[ProductOption]:
        return (
            db.query(self.model)
            .filter(ProductOption.product_id == product_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


product_option = CRUDProductOption(ProductOption)
