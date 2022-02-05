from fastapi import HTTPException


def validate_search_params(skip: int = None) -> None:
    if skip and skip < 0:
        raise HTTPException(
            status_code=400, detail="Skip must be positive",
        )
