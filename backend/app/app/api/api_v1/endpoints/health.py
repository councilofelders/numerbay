"""Health check endpoints."""

from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
def healthz() -> Dict[str, str]:
    """Return a simple liveness response for Cloud Run checks."""

    return {"status": "ok"}
