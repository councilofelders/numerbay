""" Injection dependencies for endpoints """

from typing import Dict, Generator, Optional

import google.auth.transport.requests
import google.oauth2.id_token
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from google.cloud import storage
from google.cloud.storage import Bucket
from jose import jwt
from pydantic import ValidationError
from requests import Response
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    """Get db session"""

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    Get current user

    Args:
        db (Session): db session
        token: auth token

    Returns:
        models.User: current user
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if token_data.type is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.token_version != (token_data.ver or 0):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Session expired, please log in again",
        )
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Get current active user

    Args:
        current_user (models.User): current user

    Returns:
        models.User: current active user
    """

    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Get current active superuser

    Args:
        current_user (models.User): current user

    Returns:
        models.User: current active superuser
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_gcs_bucket() -> Bucket:
    """Get GCS bucket"""
    client = storage.Client()
    bucket = client.bucket(settings.GCP_STORAGE_BUCKET)
    # bucket.cors = [
    #     {
    #         "origin": ["*"],
    #         "responseHeader": [
    #             "Content-Type",
    #             "Access-Control-Allow-Origin",
    #             "X-Requested-With",
    #             "x-goog-resumable",
    #             "cache-control",
    #         ],
    #         "method": ["GET", "PUT", "POST", "OPTIONS"],
    #         "maxAgeSeconds": 3600,
    #     }
    # ]
    # bucket.patch()
    # print(f"{settings.GCP_STORAGE_BUCKET} Cors: {bucket.cors}")
    return bucket


def make_gcp_authorized_post_request(
    endpoint: str,
    audience: str,
    payload: Optional[Dict] = None,
    headers: Optional[Dict] = None,
) -> Response:
    """
    Make a POST request to the specified HTTP endpoint with google-auth
    """
    if headers is None:
        headers = {}

    auth_req = google.auth.transport.requests.Request()
    token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
    headers = {**headers, "Authorization": f"Bearer {token}"}

    response = requests.post(endpoint, json=payload, headers=headers, timeout=120)

    return response
