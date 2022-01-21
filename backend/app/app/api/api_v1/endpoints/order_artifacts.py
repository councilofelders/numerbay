import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from google.api_core.exceptions import NotFound
from google.cloud.storage import Bucket
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies.artifacts import (
    get_object_name,
    send_artifact_emails_for_active_orders,
    validate_existing_artifact,
    validate_new_artifact,
)
from app.api.dependencies.products import (
    validate_buyer,
    validate_existing_product,
)
from app.core.celery_app import celery_app
from app.core.config import settings

router = APIRouter()


@router.post("/generate-upload-url")
def generate_upload_url(
    *,
    order_id: int = Form(...),
    filename: str = Form(...),
    filesize: int = Form(None),
    action: str = Form(None),
    filename_suffix: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # product = crud.product.get(db, id=product_id)
    # validate_new_artifact(
    #     product=product, current_user=current_user, url=None, filename=filename
    # )

    order = crud.order.get(db, id=order_id)
    product = order.product

    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, please try again after the round submission deadline",
        )

    selling_round = globals.selling_round  # type: ignore

    object_name = get_object_name(
        sku=product.sku,  # type: ignore
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
    )
    artifact = crud.order_artifact.create(db=db, obj_in=artifact_in)
    if not artifact:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create artifact",
        )

    # Check upload later after link expires
    # celery_app.send_task(
    #     "app.worker.validate_artifact_upload_task",
    #     kwargs=dict(artifact_id=artifact.id),
    #     countdown=settings.ARTIFACT_UPLOAD_URL_EXPIRE_MINUTES * 60,
    # )

    return {"id": artifact.id, "url": url}


@router.post("/{artifact_id}/validate-upload")
def validate_upload(
    *,
    artifact_id: str,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    globals = crud.globals.get_singleton(db=db)
    selling_round = globals.selling_round  # type: ignore

    artifact = crud.order_artifact.get(db, id=artifact_id)
    # artifact = validate_existing_artifact(
    #     artifact=artifact, product_id=product_id, selling_round=selling_round
    # )

    # product = crud.product.get(db, id=product_id)
    # validate_new_artifact(
    #     product=product, current_user=current_user, url=artifact.url, filename=artifact.object_name  # type: ignore
    # )

    if not artifact.object_name:
        raise HTTPException(
            status_code=400, detail="Artifact not an upload object",
        )

    blob = bucket.blob(artifact.object_name)
    if not blob.exists():
        raise HTTPException(
            status_code=404, detail="Artifact file not uploaded",
        )

    crud.order_artifact.update(db, db_obj=artifact, obj_in={"state": "active"})

    # mark product as ready
    # if product:
    #     if not product.is_ready:
    #         crud.product.update(db, db_obj=product, obj_in={"is_ready": True})

    # validate and fulfill orders immediately
    # celery_app.send_task(
    #     "app.worker.validate_artifact_upload_task",
    #     kwargs=dict(artifact_id=artifact.id, skip_if_active=False),
    # )

    return artifact


# @router.post("/", response_model=schemas.OrderArtifact)
# async def create_product_artifact(
#     *,
#     order_id: int,
#     url: str = Body(...),
#     description: str = Body(None),
#     # filename: str = Body(None),
#     db: Session = Depends(deps.get_db),
#     # driver: StorageDriver = Depends(deps.get_cloud_storage_driver),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     product = crud.product.get(db, id=product_id)
#
#     validate_new_artifact(
#         product=product, current_user=current_user, url=url, filename=None
#     )
#
#     all_modes = [option.mode for option in product.options]  # type: ignore
#
#     if "stake" in all_modes or "stake_with_limit" in all_modes:
#         raise HTTPException(
#             status_code=400,
#             detail="Stake modes require native artifact uploads for automated submissions",
#         )
#
#     # not during round rollover
#     globals = crud.globals.get_singleton(db=db)
#     if globals.is_doing_round_rollover:  # type: ignore
#         raise HTTPException(
#             status_code=400,
#             detail="Round rollover in progress, please try again after the round submission deadline",
#         )
#
#     selling_round = globals.selling_round  # type: ignore
#
#     # Create artifact
#     artifact_in = schemas.OrderArtifactCreate(
#         product_id=product_id,
#         date=datetime.utcnow(),
#         round_tournament=selling_round,
#         description=description,
#         url=url,
#         # object_name=object_name,
#     )
#     artifact = crud.order_artifact.create(db=db, obj_in=artifact_in)
#
#     # mark product as ready
#     if product:
#         if not product.is_ready:
#             crud.product.update(db, db_obj=product, obj_in={"is_ready": True})
#
#     # Send notification emails
#     send_artifact_emails_for_active_orders(db, artifact, is_file=False)
#     return artifact


# @router.put("/{artifact_id}")
# async def update_product_artifact(
#     *,
#     artifact_id: str,
#     description: str = Body(None),
#     url: str = Body(None),
#     filename: str = Body(None),
#     db: Session = Depends(deps.get_db),
#     # driver: StorageDriver = Depends(deps.get_cloud_storage_driver),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     product = crud.product.get(db, id=product_id)
#     validate_new_artifact(
#         product=product, current_user=current_user, url=url, filename=filename
#     )
#
#     # not during round rollover
#     globals = crud.globals.get_singleton(db=db)
#     if globals.is_doing_round_rollover:  # type: ignore
#         raise HTTPException(
#             status_code=400,
#             detail="Round rollover in progress, please try again after the round submission deadline",
#         )
#
#     selling_round = globals.selling_round  # type: ignore
#
#     artifact = crud.order_artifact.get(db, id=artifact_id)
#     artifact = validate_existing_artifact(
#         artifact=artifact, product_id=product_id, selling_round=selling_round
#     )
#
#     # object_name = None
#     # if file_obj:
#     #     object_name = get_object_name(sku=product.sku, selling_round=selling_round, original_filename=file_obj.filename,
#     #                                   override_filename=filename)
#     #     upload_obj = upload_file(driver=driver, file_obj=file_obj, object_name=object_name)
#     #     if not upload_obj:
#     #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #                             detail="File could not be uploaded")
#
#     # Update artifact
#     artifact_dict = {}
#     artifact_dict["description"] = description
#     if url:
#         artifact_dict["url"] = url
#     # if file_obj:
#     #     artifact_dict['object_name'] = object_name
#
#     artifact = crud.order_artifact.update(db=db, db_obj=artifact, obj_in=artifact_dict)
#     return artifact


@router.get(
    "/",
    response_model=Dict[str, Union[int, List[schemas.OrderArtifact]]],
)
def list_order_artifacts(
    *,
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    # if product.owner_id != current_user.id and not validate_buyer(
    #     product, current_user, selling_round
    # ):
    #     raise HTTPException(status_code=403, detail="Not enough permissions")

    artifacts = crud.order_artifact.get_multi_by_order_round(
        db, order=order, round_tournament=selling_round
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
    # product = crud.product.get(db=db, id=product_id)
    # if not product:
    #     raise HTTPException(status_code=404, detail="Product not found")

    # selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    # is_seller = product.owner_id == current_user.id
    # order = validate_buyer(product, current_user, selling_round)

    # # owner or buyer
    # if not is_seller and not order:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")
    #
    # # file mode
    # if order and not is_seller and order.mode != "file":
    #     raise HTTPException(
    #         status_code=403, detail="Download not allowed for this artifact"
    #     )

    artifact = crud.order_artifact.get(db, id=artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    if not artifact.object_name:
        raise HTTPException(status_code=400, detail="Artifact not an upload")

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


@router.delete("/{artifact_id}", response_model=schemas.OrderArtifact)
def delete_product_artifact(
    *,
    artifact_id: str,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an artifact.
    """
    # product ownership
    # validate_existing_product(
    #     db, product_id=product_id, currend_user_id=current_user.id
    # )

    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, please try again after the round submission deadline",
        )

    selling_round = globals.selling_round  # type: ignore

    artifact = crud.order_artifact.get(db, id=artifact_id)
    # validate_existing_artifact(
    #     artifact=artifact, product_id=product_id, selling_round=selling_round
    # )

    artifact = crud.order_artifact.remove(db=db, id=artifact_id)
    object_name = artifact.object_name
    if object_name:
        try:
            blob = bucket.blob(object_name)
            blob.delete()
        except NotFound:
            pass
    return artifact
