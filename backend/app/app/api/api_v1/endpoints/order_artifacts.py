import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, Form, HTTPException, status
from google.api_core.exceptions import NotFound
from google.cloud.storage import Bucket
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.order_artifacts import (  # send_artifact_emails_for_active_orders,
    get_object_name,
    validate_existing_order_artifact,
    validate_new_order_artifact,
)
from app.api.dependencies.products import validate_buyer, validate_existing_product
from app.core.celery_app import celery_app
from app.core.config import settings
from app.utils import send_failed_artifact_seller_email

router = APIRouter()


@router.post("/generate-upload-url")
def generate_upload_url(
    *,
    order_id: int = Form(...),
    filename: str = Form(...),
    is_numerai_direct: str = Form(None),
    filesize: int = Form(None),
    action: str = Form(None),
    filename_suffix: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    if is_numerai_direct in ["true", "True"]:
        is_numerai_direct = True  # type: ignore
    else:
        is_numerai_direct = False  # type: ignore

    order = crud.order.get(db, id=order_id)
    validate_new_order_artifact(
        order=order, current_user=current_user, url=None, filename=filename
    )

    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, "
            "please try again after the round submission deadline",
        )

    selling_round = globals.selling_round  # type: ignore

    object_name = get_object_name(
        sku=order.product.sku,  # type: ignore
        selling_round=selling_round,
        original_filename=filename,
        override_filename=filename_suffix,
    )

    if not action:
        action = "PUT"
    if action.upper() not in ["PUT", "POST"]:
        raise HTTPException(
            status_code=400, detail="Action type must be either PUT or POST for uploads"
        )

    if is_numerai_direct:
        # submit to Numerai directly
        # todo handle stake mode and no submit id
        submission_auth = numerai.generate_numerai_submission_url(
            object_name=object_name,
            model_id=order.submit_model_id,  # type: ignore
            tournament=order.product.model.tournament,  # type: ignore
            numerai_api_key_public_id=order.buyer.numerai_api_key_public_id,  # type: ignore
            numerai_api_key_secret=order.buyer.numerai_api_key_secret,  # type: ignore
        )
        url, object_name = submission_auth["url"], submission_auth["filename"]
    else:
        # upload for buyer
        blob = bucket.blob(object_name)
        url = blob.generate_signed_url(
            expiration=timedelta(minutes=settings.ARTIFACT_UPLOAD_URL_EXPIRE_MINUTES),
            content_type="application/octet-stream",
            bucket_bound_hostname=(
                "https://storage.numerbay.ai"
                if settings.GCP_STORAGE_BUCKET == "storage.numerbay.ai"
                else None
            ),
            method=action,
            version="v4",
        )

    # Create artifact
    artifact_in = schemas.OrderArtifactCreate(
        id=uuid.uuid4().hex,
        order_id=order_id,
        date=datetime.utcnow(),
        round_tournament=selling_round,
        description=description,
        url=None,
        object_name=object_name,
        object_size=filesize,
        is_numerai_direct=is_numerai_direct,
    )
    artifact = crud.order_artifact.create(db=db, obj_in=artifact_in)
    if not artifact:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create artifact",
        )

    return {
        "id": artifact.id,
        "url": url,
        "buyer_public_key": order.buyer_public_key,  # type: ignore
    }


@router.post("/{artifact_id}/validate-upload")
def validate_upload(
    *,
    artifact_id: str,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    artifact = crud.order_artifact.get(db, id=artifact_id)
    artifact = validate_existing_order_artifact(
        artifact=artifact, selling_round=selling_round
    )

    if not artifact.object_name:
        raise HTTPException(
            status_code=400, detail="Artifact not an upload object",
        )

    if artifact.is_numerai_direct:
        # validate numerai submission
        # todo handling everything
        submission_id = numerai.validate_numerai_submission(
            object_name=artifact.object_name,
            model_id=artifact.order.submit_model_id,  # type: ignore
            tournament=artifact.order.product.model.tournament,  # type: ignore
            numerai_api_key_public_id=artifact.order.buyer.numerai_api_key_public_id,
            numerai_api_key_secret=artifact.order.buyer.numerai_api_key_secret,
        )
        if submission_id is None:
            if settings.EMAILS_ENABLED:
                # Send failed artifact email notification to seller
                if artifact.order.product.owner.email:
                    send_failed_artifact_seller_email(
                        email_to=artifact.order.product.owner.email,  # type: ignore
                        username=artifact.order.product.owner.username,
                        round_tournament=artifact.round_tournament,  # type: ignore
                        product=artifact.order.product.sku,
                        artifact=artifact.object_name,
                    )

            crud.order_artifact.update(db, db_obj=artifact, obj_in={"state": "failed"})
            crud.order.update(
                db, db_obj=artifact.order, obj_in={"submit_state": "failed"}
            )  # type: ignore
            raise HTTPException(
                status_code=404, detail="Submission failed",
            )
        crud.order.update(
            db,
            db_obj=artifact.order,
            obj_in={"submit_state": "completed", "last_submit_round": selling_round},
        )  # type: ignore
        artifact = crud.order_artifact.get(db, id=artifact_id)
    else:
        # validate numerbay upload
        blob = bucket.blob(artifact.object_name)
        if not blob.exists():
            if settings.EMAILS_ENABLED:
                # Send failed artifact email notification to seller
                if artifact.order.product.owner.email:
                    send_failed_artifact_seller_email(
                        email_to=artifact.order.product.owner.email,  # type: ignore
                        username=artifact.order.product.owner.username,
                        round_tournament=artifact.round_tournament,  # type: ignore
                        product=artifact.order.product.sku,
                        artifact=artifact.object_name,  # type: ignore
                    )

            crud.order_artifact.update(db, db_obj=artifact, obj_in={"state": "failed"})
            raise HTTPException(
                status_code=404, detail="Artifact file not uploaded",
            )

        celery_app.send_task(
            "app.worker.send_new_order_artifact_emails_task",
            kwargs=dict(artifact_id=artifact.id),
        )

    crud.order_artifact.update(
        db, db_obj=artifact, obj_in={"state": "active"}  # type: ignore
    )

    # mark product as ready
    # if not artifact.order.product.is_ready:  # type: ignore
    #     crud.product.update(
    #         db, db_obj=artifact.order.product, obj_in={"is_ready": True}  # type: ignore
    #     )

    # validate and fulfill orders immediately
    # celery_app.send_task(
    #     "app.worker.validate_artifact_upload_task",
    #     kwargs=dict(artifact_id=artifact.id, skip_if_active=False),
    # )

    # todo email notification

    return artifact


@router.get(
    "/", response_model=Dict[str, Union[int, List[schemas.OrderArtifact]]],
)
def list_order_artifacts(
    *,
    order_id: int,
    active_only: Optional[bool] = False,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    if order.product.owner_id != current_user.id and not validate_buyer(
        order.product, current_user, selling_round
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    artifacts = crud.order_artifact.get_multi_by_order_round(
        db, order=order, round_tournament=selling_round, active_only=active_only
    )
    return {"total": len(artifacts), "data": artifacts}


@router.get("/{artifact_id}/generate-download-url")
def generate_download_url(
    *,
    artifact_id: str,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    artifact = crud.order_artifact.get(db, id=artifact_id)

    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    if not artifact.object_name:
        raise HTTPException(status_code=400, detail="Artifact not an upload")
    if artifact.is_numerai_direct:
        raise HTTPException(
            status_code=400, detail="Download not allowed for this artifact"
        )

    order = artifact.order
    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
    is_seller = order.product.owner_id == current_user.id
    order = validate_buyer(order.product, current_user, selling_round)  # type: ignore

    # owner or buyer
    if not is_seller and not order:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # file mode
    if order and not is_seller and order.mode != "file":
        raise HTTPException(
            status_code=403, detail="Download not allowed for this artifact"
        )

    action = "GET"
    blob = bucket.blob(artifact.object_name)
    url = blob.generate_signed_url(
        expiration=timedelta(minutes=settings.ARTIFACT_DOWNLOAD_URL_EXPIRE_MINUTES),
        # content_type='application/octet-stream',
        bucket_bound_hostname=(
            "https://storage.numerbay.ai"
            if settings.GCP_STORAGE_BUCKET == "storage.numerbay.ai"
            else None
        ),
        method=action,
        version="v4",
    )
    return url


@router.get("/{artifact_id}", response_model=schemas.OrderArtifact)
def get_order_artifact(
    *,
    artifact_id: str,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get an artifact.
    """
    artifact = crud.order_artifact.get(db, id=artifact_id)

    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    if not artifact.object_name:
        raise HTTPException(status_code=400, detail="Artifact not an upload")

    order = artifact.order
    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
    is_seller = order.product.owner_id == current_user.id
    order = validate_buyer(order.product, current_user, selling_round)  # type: ignore

    # owner or buyer
    if not is_seller and not order:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return artifact


@router.delete("/{artifact_id}", response_model=schemas.OrderArtifact)
def delete_order_artifact(
    *,
    artifact_id: str,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an artifact.
    """
    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, "
            "please try again after the round submission deadline",
        )

    selling_round = globals.selling_round  # type: ignore

    artifact = crud.order_artifact.get(db, id=artifact_id)
    validate_existing_order_artifact(artifact=artifact, selling_round=selling_round)

    # product ownership
    validate_existing_product(
        db, product_id=artifact.order.product_id, currend_user_id=current_user.id  # type: ignore
    )

    artifact = crud.order_artifact.remove(db=db, id=artifact_id)  # type: ignore
    object_name = artifact.object_name
    if object_name:
        try:
            blob = bucket.blob(object_name)
            blob.delete()
        except NotFound:
            pass
    return artifact