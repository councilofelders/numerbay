import functools
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.models import Artifact, Order, Product

router = APIRouter()


# @router.post("/fill-product-mode")
# def fill_product_mode(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Fill product mode (for db migration only).
#     """
#     db.query(Product).filter(Product.is_on_platform).update(
#         {Product.mode: "file"}, synchronize_session=False
#     )
#     db.commit()
#     return {"msg": "success!"}


@router.post("/refresh-sales-stats")
def refresh_sales_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Calculate sales stats for all products (for db migration only).
    """
    products = db.query(Product).filter(Product.is_on_platform).all()
    for product in products:
        query_filters = [Order.product_id == product.id, Order.state == "confirmed"]
        query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
        orders = db.query(Order).filter(query_filter).order_by(desc(Order.id)).all()
        if orders and len(orders) > 0:
            product.total_num_sales = len(orders)
            product.last_sale_price = orders[0].price
            if len(orders) > 1:
                product.last_sale_price_delta = (
                    product.last_sale_price - orders[1].price
                )
    db.commit()
    return {"msg": "success!"}


@router.post("/remove-failed-uploads")
def remove_failed_uploads(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Remove failed uploads (for db migration only).
    """
    artifacts = db.query(Artifact).filter(Artifact.object_name.is_not(None))  # type: ignore
    for artifact in artifacts:
        bucket = deps.get_gcs_bucket()
        blob = bucket.blob(artifact.object_name)
        if not blob.exists():
            print(
                f"Remove artifact {artifact.object_name} for product {artifact.product.name}"
            )
            db.delete(artifact)
    db.commit()
    return {"msg": "success!"}


@router.post("/update-artifact-states")
def update_artifact_states(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update artifact states (for db migration only).
    """
    globals = crud.globals.update_singleton(db)
    selling_round = globals.selling_round  # type: ignore

    artifacts = db.query(Artifact)
    for artifact in artifacts:
        if (
            artifact.round_tournament < selling_round
            and artifact.product.category.is_per_round
        ):
            artifact.state = "expired"
            continue

        if artifact.object_name:
            bucket = deps.get_gcs_bucket()
            blob = bucket.blob(artifact.object_name)
            if not blob.exists():
                artifact.state = "failed"
                continue
        artifact.state = "active"
    db.commit()
    return {"msg": "success!"}


@router.post("/fill-product-readiness")
def fill_product_readiness(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Fill product readiness (for db migration only).
    """
    globals = crud.globals.update_singleton(db)
    selling_round = globals.selling_round  # type: ignore

    products = db.query(Product).filter(Product.is_on_platform).all()
    for product in products:
        artifacts = crud.artifact.get_multi_by_product_round(
            db, product=product, round_tournament=selling_round
        )
        product.is_ready = len(artifacts) > 0
    db.commit()
    return {"msg": "success!"}


# @router.post("/fix-product-models")
# def fix_product_models(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Fix product model foreign keys (for db migration only).
#     """
#     # match_statement = select([Product.id, Product.name, Model.id]).where(Product.name == Model.name)
#     db.query(Product).filter(Product.name == Model.name).update(
#         {Product.model_id: Model.id}, synchronize_session=False
#     )
#     db.commit()
#     return {"msg": "success!"}


# @router.post("/fix-signals-models")
# def fix_signals_models(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Fix product model foreign keys (for db migration only).
#     """
#     # match_statement = select([Product.id, Product.name, Model.id]).where(Product.name == Model.name)
#     signals_products = db.query(Product).filter(Product.category_id == 6).all()
#     product_to_return = []
#     for product in signals_products:
#         model = (
#             db.query(Model)
#             .filter(and_(Model.tournament == 11, Model.name == product.name))
#             .first()
#         )
#         if model:
#             product.model_id = model.id
#             product_to_return.append(product.id)
#     db.commit()
#     # signals_products = db.query(Product).filter(Product.category_id == 6)
#     return product_to_return


# @router.post("/fix-url-encoding")
# def fix_url_encoding(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Fix url encoding (for db migration only).
#     """
#     # match_statement = select([Product.id, Product.name, Model.id]).where(Product.name == Model.name)
#     products = (
#         db.query(Product)
#         .filter(
#             or_(Product.avatar.contains(" "), Product.third_party_url.contains(" "))
#         )
#         .all()
#     )
#     for product in products:
#         if product.avatar:
#             product.avatar = product.avatar.replace(" ", "%20")
#         if product.third_party_url:
#             product.third_party_url = product.third_party_url.replace(" ", "%20")
#     db.commit()
#     return {"msg": "success!"}


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
