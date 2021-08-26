import asyncio
import sys
from datetime import datetime
from decimal import Decimal
from typing import Any, List

from app.api.api_v1.endpoints.numerai import get_numerai_models, get_numerai_model_performance
from app.db.session import SessionLocal
from app.schemas import User
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.core.apscheduler import scheduler

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
    models = crud.model.get_multi(db)
    for model in models:
        products = db.query(Product).filter(Product.name == model.name).all()
        for product in products:
            product.model_id = model.id
    db.commit()
    return {"msg": "success!"}


# NOT PUBLIC
async def fetch_single_user_models(user: User):
    models = get_numerai_models(current_user=user)
    for model in models:
        model_performance = get_numerai_model_performance(tournament=int(model['tournament']), model_name=model['name'])
        model['model_performance'] = model_performance
    return {'id': user.id, 'models': models}


@scheduler.scheduled_job('cron', id='batch_update_models', day_of_week='wed-sun')
async def batch_update_models():
    db = SessionLocal()
    try:
        print(f'{datetime.utcnow()} Running batch_update_models...')
        users = crud.user.search(db, filters={'numerai_api_key_public_id': ['any']})['data']
        tasks = []
        for user in users:
            tasks.append(fetch_single_user_models(user=user))
        all_user_models = await asyncio.gather(*tasks, return_exceptions=True)

        # ingest numerai models to db
        db_models = {}
        for user_models in all_user_models:
            try:
                for model in user_models['models']:
                    db_models[model['id']] = Model(
                        id=model['id'], name=model['name'], tournament=int(model['tournament']),
                        owner_id=int(user_models['id']),
                        nmr_staked=Decimal(model['model_performance']['nmrStaked']) if model['model_performance']['nmrStaked'] else 0,
                        start_date=model['model_performance']['startDate'],
                        latest_ranks=model['model_performance']['modelPerformance']['latestRanks'],
                        latest_reps=model['model_performance']['modelPerformance']['latestReps'],
                        latest_returns=model['model_performance']['modelPerformance']['latestReturns'],
                        round_model_performances=model['model_performance']['modelPerformance']['roundModelPerformances']
                    )
            except Exception as e:
                print(e)
            continue

        for db_model in db.query(Model).filter(Model.id.in_(db_models.keys())).all():
            # Updates
            db.merge(db_models.pop(db_model.id))

        # Inserts
        db.add_all(db_models.values())
        db.commit()

        print(f'{datetime.utcnow()} Finished batch_update_models')
    finally:
        sys.stdout.flush()
        db.close()


def read_models(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve models.
    """
    if crud.user.is_superuser(current_user):
        models = crud.model.get_multi(db, skip=skip, limit=limit)
    else:
        models = crud.model.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return models


def create_model(
    *,
    db: Session = Depends(deps.get_db),
    model_in: schemas.ModelCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new model.
    """
    model = crud.model.create_with_owner(db=db, obj_in=model_in, owner_id=current_user.id)
    return model


def update_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    model_in: schemas.ModelUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an model.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if not crud.user.is_superuser(current_user) and (model.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    model = crud.model.update(db=db, db_obj=model, obj_in=model_in)
    return model


def read_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get model by ID.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if not crud.user.is_superuser(current_user) and (model.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return model


def delete_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an model.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if not crud.user.is_superuser(current_user) and (model.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    model = crud.model.remove(db=db, id=id)
    return model
