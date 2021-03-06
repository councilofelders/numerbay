""" Dependencies for order artifacts endpoints """

import uuid
from datetime import timedelta
from pathlib import Path
from typing import Optional

from fastapi import HTTPException
from google.cloud.storage import Bucket
from sqlalchemy.orm import Session

from app import crud, models
from app.core.config import settings
from app.utils import send_new_artifact_email, send_new_artifact_seller_email


def get_object_name(
    sku: str, selling_round: int, original_filename: str, override_filename: str = None
) -> str:
    """Get object name"""
    file_ext = Path(original_filename).suffix
    object_name = f"{sku}_{str(selling_round)}_{uuid.uuid4().hex}"
    if override_filename:
        object_name += f"_{override_filename}"
    object_name += file_ext
    return object_name


def generate_gcs_signed_url(
    bucket: Bucket,
    object_name: str,
    action: str = "PUT",
    expiration_minutes: int = 10,
    is_upload: bool = True,
) -> str:
    """Generate GCS signed URL"""
    blob = bucket.blob(object_name)
    url = blob.generate_signed_url(
        expiration=timedelta(minutes=expiration_minutes),
        content_type="application/octet-stream" if is_upload else None,
        bucket_bound_hostname=(
            "https://storage.numerbay.ai"
            if settings.GCP_STORAGE_BUCKET == "storage.numerbay.ai"
            else None
        ),
        method=action,
        version="v4",
    )
    return url


def validate_new_order_artifact(
    order: Optional[models.Order],
    current_user: models.User,
    filename: str = None,
) -> None:
    """Validate new order artifact"""
    # Order exists
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    # Product ownership
    if order.product.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    # todo filename suffix / desc validation

    # todo duplicate artifact

    # todo test


def validate_existing_order_artifact(
    artifact: Optional[models.OrderArtifact], selling_round: int
) -> models.OrderArtifact:
    """Validate existing order artifact"""
    # artifact exists
    if not artifact:
        raise HTTPException(
            status_code=404,
            detail="Order artifact not found",
        )

    # artifact current round
    if (
        artifact.order.product.category.is_per_round  # type: ignore
        and artifact.round_tournament < selling_round  # type: ignore
    ):
        raise HTTPException(
            status_code=400,
            detail="Order artifact expired",
        )
    return artifact


def send_artifact_emails_for_active_orders(
    db: Session, artifact: models.Artifact
) -> None:
    """Send artifact emails for active orders"""
    if settings.EMAILS_ENABLED:
        # orders = crud.order.get_multi_by_state(
        #     db, state="confirmed", round_order=globals.selling_round  # type: ignore
        # )
        orders = crud.order.get_active_orders(
            db, round_order=crud.globals.get_singleton(db=db).selling_round  # type: ignore
        )
        for order in orders:
            if order.product_id == artifact.product_id:
                # Send new artifact email notifications to buyers
                if order.buyer.email:
                    send_new_artifact_email(
                        email_to=order.buyer.email,
                        username=order.buyer.username,
                        round_order=order.round_order,
                        product=order.product.sku,
                        order_id=order.id,
                        artifact=artifact.object_name,  # type: ignore
                    )

        # Send new artifact email notification to seller
        if artifact.product.owner.email:
            send_new_artifact_seller_email(
                email_to=artifact.product.owner.email,
                username=artifact.product.owner.username,
                round_tournament=artifact.round_tournament,  # type: ignore
                product=artifact.product.sku,
                artifact=artifact.object_name,  # type: ignore
            )
