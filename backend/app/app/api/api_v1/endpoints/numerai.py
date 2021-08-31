from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List)
def get_numerai_models(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve products.
    """
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
    """
    Retrieve products.
    """
    if tournament not in [8, 11]:
        raise HTTPException(status_code=404, detail="Tournament not found")
    try:
        data = crud.model.get_numerai_model_performance(
            tournament=tournament, model_name=model_name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Numerai API Error: " + str(e))
    return data
