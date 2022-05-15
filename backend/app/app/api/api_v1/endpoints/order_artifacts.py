""" Order artifacts endpoints """

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, Form, HTTPException, status
from google.api_core.exceptions import NotFound
from google.cloud.storage import Bucket
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.order_artifacts import (  # send_artifact_emails_for_active_orders,
    generate_gcs_signed_url,
    get_object_name,
    validate_existing_order_artifact,
    validate_new_order_artifact,
)
from app.api.dependencies.orders import validate_existing_order
from app.api.dependencies.products import validate_buyer, validate_product_owner
from app.api.dependencies.site_globals import validate_not_during_rollover
from app.core.celery_app import celery_app
from app.core.config import settings
from app.utils import send_failed_artifact_seller_email

router = APIRouter()


@router.post("/generate-upload-url")
def generate_upload_url(  # pylint: disable=too-many-locals
    *,
    order_id: int = Form(..., description="order ID"),
    filename: str = Form(..., description="file name"),
    is_numerai_direct: str = Form(
        None, description="whether this is direct Numerai submission"
    ),
    filesize: int = Form(None, description="file size"),
    action: str = Form(None, description="method for upload"),
    filename_suffix: str = Form(None, description="file name suffix"),
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Generate upload URL"""
    if is_numerai_direct in [  # pylint: disable=simplifiable-if-statement
        "true",
        "True",
    ]:
        is_numerai_direct = True  # type: ignore
    else:
        is_numerai_direct = False  # type: ignore

    order = crud.order.get(db, id=order_id)
    validate_new_order_artifact(
        order=order, current_user=current_user, filename=filename
    )

    # not during round rollover
    site_globals = validate_not_during_rollover(db)

    selling_round = site_globals.selling_round

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
        if not order.submit_model_id:  # type: ignore
            raise HTTPException(
                status_code=400,
                detail="The order did not designate a Numerai submission slot",
            )

        submission_auth = numerai.generate_numerai_submission_url(
            object_name=object_name,
            model_id=order.submit_model_id,  # type: ignore
            tournament=order.product.model.tournament,  # type: ignore
            numerai_api_key_public_id=order.buyer.numerai_api_key_public_id,  # type: ignore
            numerai_api_key_secret=order.buyer.numerai_api_key_secret,  # type: ignore
        )
        url, object_name = submission_auth["url"], submission_auth["filename"]
    else:
        if order.mode != "file":  # type: ignore
            raise HTTPException(
                status_code=400,
                detail="Uploading for buyer is not allowed for stake mode order",
            )
        # upload for buyer
        url = generate_gcs_signed_url(
            bucket=bucket,
            object_name=object_name,
            action=action,
            expiration_minutes=settings.ARTIFACT_UPLOAD_URL_EXPIRE_MINUTES,
            is_upload=True,
        )

    # Create artifact
    artifact_in = schemas.OrderArtifactCreate(
        id=uuid.uuid4().hex,
        order_id=order_id,
        date=datetime.utcnow(),
        round_tournament=selling_round,
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
    current_user: models.User = Depends(
        deps.get_current_active_user
    ),  # pylint: disable=W0613
) -> Any:
    """Validate upload"""
    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    artifact = crud.order_artifact.get(db, id=artifact_id)
    artifact = validate_existing_order_artifact(
        artifact=artifact, selling_round=selling_round
    )

    if not artifact.object_name:
        raise HTTPException(
            status_code=400,
            detail="Artifact not an upload object",
        )

    if artifact.is_numerai_direct:
        # validate numerai submission
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
                status_code=404,
                detail="Submission failed",
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
                status_code=404,
                detail="Artifact file not uploaded",
            )

        celery_app.send_task(
            "app.worker.send_new_order_artifact_emails_task",
            kwargs=dict(artifact_id=artifact.id),
        )

    crud.order_artifact.update(
        db, db_obj=artifact, obj_in={"state": "active"}  # type: ignore
    )

    # mark product as ready
    product = crud.product.get(db, id=artifact.order.product_id)  # type: ignore
    if product:
        if not product.is_ready:
            crud.product.update(db, db_obj=product, obj_in={"is_ready": True})

    return artifact


@router.get(
    "/",
    response_model=Dict[str, Union[int, List[schemas.OrderArtifact]]],
)
def list_order_artifacts(
    *,
    order_id: int,
    active_only: Optional[bool] = False,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """List order artifacts"""
    order = validate_existing_order(db, order_id)

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
    """Generate download URL"""
    artifact = crud.order_artifact.get(db, id=artifact_id)

    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    if not artifact.object_name:
        raise HTTPException(status_code=400, detail="Artifact not an upload")
    if artifact.is_numerai_direct:
        raise HTTPException(
            status_code=400, detail="Direct Numerai submission cannot be downloaded"
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
    url = generate_gcs_signed_url(
        bucket=bucket,
        object_name=artifact.object_name,
        action=action,
        expiration_minutes=settings.ARTIFACT_DOWNLOAD_URL_EXPIRE_MINUTES,
        is_upload=False,
    )
    return url


@router.get("/{artifact_id}", response_model=schemas.OrderArtifact)
def get_order_artifact(
    *,
    artifact_id: str,
    db: Session = Depends(deps.get_db),
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
    site_globals = validate_not_during_rollover(db)

    selling_round = site_globals.selling_round

    artifact = crud.order_artifact.get(db, id=artifact_id)

    validate_existing_order_artifact(artifact=artifact, selling_round=selling_round)

    # not numerai direct submission
    if artifact.is_numerai_direct:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Direct Numerai submission cannot be deleted",
        )

    # product ownership
    validate_product_owner(
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
