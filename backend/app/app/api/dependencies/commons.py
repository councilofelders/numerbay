""" Dependencies for multiple endpoints """

from fastapi import HTTPException


def validate_search_params(skip: int = None) -> None:
    """Validate search params"""
    if skip and skip < 0:
        raise HTTPException(
            status_code=400,
            detail="Skip must be positive",
        )
