""" CRUD for category """

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, aliased

from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    """ CRUD for category """

    def get_all_subcategories(self, db: Session, *, category_id: int) -> List:
        """ Get all subcategories """
        nodealias = aliased(self.model)

        descendants = (
            db.query(self.model)
            .filter(Category.id == category_id)
            .cte(name="items", recursive=True)
        )

        descendants = descendants.union(
            db.query(nodealias).join(descendants, nodealias.parent)
        )

        return db.query(descendants).all()

    def get_multi_by_slug(
        self, db: Session, *, slug: str, skip: int = 0, limit: int = None
    ) -> List[Category]:
        """ Get multiple categories by slug """
        return (
            db.query(self.model)
            .filter(Category.slug == slug)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_parent(
        self, db: Session, *, obj_in: CategoryCreate, parent_id: int
    ) -> Category:
        """ Create category with parent """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, parent_id=parent_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


category = CRUDCategory(Category)
