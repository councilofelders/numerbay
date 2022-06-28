""" Numerai-related endpoints """

from decimal import Decimal
from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException

from app import models
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.numerai import fill_missing_round_performances

router = APIRouter()


@router.get("/", response_model=List)
def get_numerai_models_endpoint(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get Numerai models"""

    if (
        current_user.numerai_api_key_secret is None
        or len(current_user.numerai_api_key_secret) == 0
    ):
        raise HTTPException(
            status_code=403,
            detail="Numerai API Key is required to perform this action",
        )
    try:
        all_models = numerai.get_numerai_models(
            public_id=current_user.numerai_api_key_public_id,  # type: ignore
            secret_key=current_user.numerai_api_key_secret,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Numerai API Error: " + str(e) + " Please try changing the API key.",
        )
    return all_models


@router.get("/{tournament}/pipeline-status", response_model=Dict)
def get_numerai_pipeline_status_endpoint(tournament: int) -> Any:
    """Get Numerai scoring pipeline status"""
    if tournament not in [8, 11]:
        raise HTTPException(status_code=404, detail="Tournament not found")
    try:
        data = numerai.get_numerai_pipeline_status(tournament=tournament)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Numerai API Error: " + str(e))
    return data


@router.get("/{tournament}/{model_name}", response_model=Dict)
def get_numerai_model_performance_endpoint(tournament: int, model_name: str) -> Any:
    """Get Numerai model performance"""
    if tournament not in [8, 11]:
        raise HTTPException(status_code=404, detail="Tournament not found")
    try:
        data = numerai.get_numerai_model_performance(
            tournament=tournament, model_name=model_name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Numerai API Error: " + str(e))
    data = fill_missing_round_performances(data)
    return data


@router.get("/{tournament}/{model_name}/target-stake", response_model=Dict)
def get_numerai_model_target_stake(
    tournament: int,
    model_name: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict:
    """Get Numerai model target stake"""
    if (
        current_user.numerai_api_key_secret is None
        or len(current_user.numerai_api_key_secret) == 0
    ):
        raise HTTPException(
            status_code=403,
            detail="Numerai API Key is required to perform this action",
        )
    try:
        target_stake = numerai.get_target_stake(
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
    """Set Numerai model target stake"""
    if (
        current_user.numerai_api_key_secret is None
        or len(current_user.numerai_api_key_secret) == 0
    ):
        raise HTTPException(
            status_code=403,
            detail="Numerai API Key is required to perform this action",
        )
    try:
        result_stake = numerai.set_target_stake(
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
