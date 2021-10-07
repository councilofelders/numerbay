from decimal import Decimal
from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List)
def get_numerai_models(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    if (
        current_user.numerai_api_key_secret is None
        or len(current_user.numerai_api_key_secret) == 0
    ):
        raise HTTPException(
            status_code=403,
            detail="Numerai API Key is required to perform this action",
        )
    try:
        all_models = crud.model.get_numerai_models(
            public_id=current_user.numerai_api_key_public_id,  # type: ignore
            secret_key=current_user.numerai_api_key_secret,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Numerai API Error: " + str(e) + " Please try changing the API key.",
        )
    return all_models


@router.get("/{tournament}/{model_name}", response_model=Dict)
def get_numerai_model_performance(tournament: int, model_name: str) -> Any:
    if tournament not in [8, 11]:
        raise HTTPException(status_code=404, detail="Tournament not found")
    try:
        data = crud.model.get_numerai_model_performance(
            tournament=tournament, model_name=model_name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Numerai API Error: " + str(e))
    return data


@router.get("/{tournament}/{model_name}/target-stake", response_model=Dict)
def get_numerai_model_target_stake(
    tournament: int,
    model_name: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict:
    if (
        current_user.numerai_api_key_secret is None
        or len(current_user.numerai_api_key_secret) == 0
    ):
        raise HTTPException(
            status_code=403,
            detail="Numerai API Key is required to perform this action",
        )
    try:
        target_stake = crud.model.get_target_stake(
            public_id=current_user.numerai_api_key_public_id,  # type: ignore
            secret_key=current_user.numerai_api_key_secret,
            tournament=tournament,
            model_name=model_name,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Numerai API Error: " + str(e) + " Please try changing the API key.",
        )
    return {"target_stake": target_stake}


@router.post("/{tournament}/{model_name}/target-stake", response_model=Dict)
def set_numerai_model_target_stake(
    tournament: int,
    model_name: str,
    target_stake_amount: Decimal = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict:
    if (
        current_user.numerai_api_key_secret is None
        or len(current_user.numerai_api_key_secret) == 0
    ):
        raise HTTPException(
            status_code=403,
            detail="Numerai API Key is required to perform this action",
        )
    try:
        result_stake = crud.model.set_target_stake(
            public_id=current_user.numerai_api_key_public_id,  # type: ignore
            secret_key=current_user.numerai_api_key_secret,
            tournament=tournament,
            model_name=model_name,
            target_stake_amount=target_stake_amount,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Numerai API Error: " + str(e) + " Please try changing the API key.",
        )
    return result_stake
