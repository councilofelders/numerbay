from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app.api import deps
from app.models import Model, Product

router = APIRouter()


# PUBLIC
@router.post("/fix-product-models")
def fix_product_models(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Fix product model foreign keys (for db migration only).
    """
    # match_statement = select([Product.id, Product.name, Model.id]).where(Product.name == Model.name)
    db.query(Product).filter(Product.name == Model.name).update(
        {Product.model_id: Model.id}, synchronize_session=False
    )
    db.commit()
    return {"msg": "success!"}


# def read_models(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve models.
#     """
#     if crud.user.is_superuser(current_user):
#         models = crud.model.get_multi(db, skip=skip, limit=limit)
#     else:
#         models = crud.model.get_multi_by_owner(
#             db=db, owner_id=current_user.id, skip=skip, limit=limit
#         )
#     return models


# def create_model(
#     *,
#     db: Session = Depends(deps.get_db),
#     model_in: schemas.ModelCreate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Create new model.
#     """
#     model = crud.model.create_with_owner(db=db, obj_in=model_in, owner_id=current_user.id)
#     return model


# def update_model(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     model_in: schemas.ModelUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an model.
#     """
#     model = crud.model.get(db=db, id=id)
#     if not model:
#         raise HTTPException(status_code=404, detail="Model not found")
#     if not crud.user.is_superuser(current_user) and (model.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     model = crud.model.update(db=db, db_obj=model, obj_in=model_in)
#     return model


# def read_model(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get model by ID.
#     """
#     model = crud.model.get(db=db, id=id)
#     if not model:
#         raise HTTPException(status_code=404, detail="Model not found")
#     if not crud.user.is_superuser(current_user) and (model.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     return model


# def delete_model(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an model.
#     """
#     model = crud.model.get(db=db, id=id)
#     if not model:
#         raise HTTPException(status_code=404, detail="Model not found")
#     if not crud.user.is_superuser(current_user) and (model.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     model = crud.model.remove(db=db, id=id)
#     return model
