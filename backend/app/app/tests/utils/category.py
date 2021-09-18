from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import CategoryCreate
from app.tests.utils.utils import random_lower_string


def create_random_category(db: Session) -> models.Category:
    name = random_lower_string()
    new_category = CategoryCreate(name=name, slug=name)
    category = crud.category.create(db, obj_in=new_category)

    return category
