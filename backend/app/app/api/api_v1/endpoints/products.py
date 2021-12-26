from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from fastapi.encoders import jsonable_encoder
from google.api_core.exceptions import NotFound
from google.cloud.storage import Bucket
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.artifacts import (
    get_object_name,
    send_artifact_emails_for_active_orders,
    validate_existing_artifact,
    validate_new_artifact,
)
from app.api.dependencies.coupons import calculate_option_price
from app.api.dependencies.products import (
    validate_buyer,
    validate_existing_product,
    validate_product_input,
)
from app.core.celery_app import celery_app
from app.core.config import settings

router = APIRouter()


@router.post(
    "/search", response_model=Dict[str, Union[int, List[schemas.Product], List, Dict]]
)
def search_products(
    db: Session = Depends(deps.get_db),
    id: int = Body(None),
    category_id: int = Body(None),
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = Body(None),
    term: str = Body(None),
    sort: str = Body(None),
    coupon: str = Body(None),
    qty: int = Body(None),
) -> Any:
    """
    Retrieve products.
    """
    products = crud.product.search(
        db,
        id=id,
        category_id=category_id,
        skip=skip,
        limit=limit,
        filters=filters,
        term=term,
        sort=sort,
    )

    products_to_return = []
    for product in products["data"]:
        product_to_return = schemas.Product.from_orm(product)
        for option in product_to_return.options:  # type: ignore
            calculate_option_price(
                option,
                coupon=None,
                coupon_obj=None,
                qty=qty if qty else 1,
                raise_exceptions=False,
            )
        products_to_return.append(product_to_return)

    products["data"] = products_to_return
    return products


@router.post(
    "/search-authenticated",
    response_model=Dict[str, Union[int, List[schemas.Product], List, Dict]],
)
def search_products_authenticated(
    db: Session = Depends(deps.get_db),
    id: int = Body(None),
    category_id: int = Body(None),
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = Body(None),
    term: str = Body(None),
    sort: str = Body(None),
    coupon: str = Body(None),
    qty: int = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve products (authenticated).
    """
    products = crud.product.search(
        db,
        id=id,
        category_id=category_id,
        skip=skip,
        limit=limit,
        filters=filters,
        term=term,
        sort=sort,
    )

    coupon_obj = crud.coupon.get_by_code(db, code=coupon)

    products_to_return = []
    for product in products["data"]:
        product_to_return = schemas.Product.from_orm(product)
        for option in product_to_return.options:  # type: ignore
            calculate_option_price(
                option,
                coupon=coupon,
                coupon_obj=coupon_obj,
                qty=qty if qty else 1,
                raise_exceptions=False,
                user=current_user,
            )
        products_to_return.append(product_to_return)

    products["data"] = products_to_return
    return products


@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new product.
    """

    # Category
    category = crud.category.get(db=db, id=product_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product_in = validate_product_input(db, product_in, category=category, current_user=current_user)  # type: ignore

    # Leaf category
    child_categories_count = (
        db.query(models.Category)
        .filter(models.Category.parent_id == category.id)
        .count()
    )
    if child_categories_count > 0:
        raise HTTPException(
            status_code=400, detail="Category must be a leaf category",
        )

    # Existing listing
    sku = f"{category.slug}-{product_in.name.lower()}"  # type: ignore
    product = crud.product.get_by_sku(db, sku=sku)
    if product:
        raise HTTPException(
            status_code=400, detail=f"{product.sku} is already listed",
        )

    # Numerai API
    numerai.check_user_numerai_api(current_user)

    # Model ownership
    tournament = category.tournament
    model_id = None
    if tournament:
        model = crud.model.get_by_name(db, name=product_in.name, tournament=tournament)
        if not model:
            raise HTTPException(
                status_code=404, detail="Model not found",
            )
        if model.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not enough permissions",
            )
        model_id = model.id

    product_options_in = product_in.options
    product_in.options = []

    # Create product
    product = crud.product.create_with_owner(
        db=db,
        obj_in=product_in,
        owner_id=current_user.id,
        sku=sku,
        model_id=model_id,
        tournament=tournament,
    )

    # Create options
    for product_option_in in product_options_in:  # type: ignore
        product_option_in.product_id = product.id
        if product_option_in.coupon_specs:
            if (
                product.id
                not in product_option_in.coupon_specs["applicable_product_ids"]
            ):
                product_option_in.coupon_specs["applicable_product_ids"].append(
                    product.id
                )
        crud.product_option.create(db, obj_in=product_option_in)

    product = crud.product.get(db, id=product.id)  # type: ignore
    return product


@router.put("/{id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    product_in: schemas.ProductUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a product.
    """
    product = validate_existing_product(
        db, product_id=id, currend_user_id=current_user.id
    )

    product_in = validate_product_input(db, product_in, category=product.category, current_user=current_user)  # type: ignore

    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, please try again after the round submission deadline",
        )

    # if hasattr(product_in, 'name') and product_in.name:
    #     raise HTTPException(
    #         status_code=400, detail="Product name cannot be changed after creation",
    #     )
    #
    # if hasattr(product_in, 'category_id') and product_in.category_id:
    #     raise HTTPException(
    #         status_code=400, detail="Product category cannot be changed after creation",
    #     )

    if product_in.options is not None:
        product_option_ids = []
        for product_option_in in product_in.options:
            if product_option_in.id is not None and product_option_in.id != -1:
                product_option_ids.append(product_option_in.id)

        for option in product.options:  # type: ignore
            if option.id not in product_option_ids:
                # deleted option
                crud.product_option.remove(db, id=option.id)

        for product_option_in in product_in.options:
            if product_option_in.id is not None and product_option_in.id != -1:
                # update option
                db_product_option = crud.product_option.get(db, id=product_option_in.id)
                if db_product_option is None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product Option {product_option_in.id} not found",
                    )
                json_product_option_in = jsonable_encoder(product_option_in)
                json_product_option_in.pop("id", None)
                json_product_option_in.pop("product_id", None)
                if (
                    json_product_option_in.get("is_on_platform", None) is None
                ):  # todo better null handling
                    json_product_option_in.pop("is_on_platform", None)
                if json_product_option_in.get("quantity", None) is None:
                    json_product_option_in.pop("quantity", None)
                if json_product_option_in.get("price", None) is None:
                    json_product_option_in.pop("price", None)
                if json_product_option_in.get("currency", None) is None:
                    json_product_option_in.pop("currency", None)
                if json_product_option_in.get("coupon", None) is None:
                    json_product_option_in.pop("coupon", None)
                if json_product_option_in.get("coupon_specs", None) is None:
                    json_product_option_in.pop("coupon_specs", None)
                else:
                    if (
                        product.id
                        not in json_product_option_in.get("coupon_specs")[
                            "applicable_product_ids"
                        ]
                    ):
                        json_product_option_in.get("coupon_specs")[
                            "applicable_product_ids"
                        ].append(product.id)
                crud.product_option.update(
                    db, db_obj=db_product_option, obj_in=json_product_option_in
                )
            else:
                # create option
                json_product_option_in = jsonable_encoder(product_option_in)
                json_product_option_in.pop("id", None)
                json_product_option_in["product_id"] = product.id
                if json_product_option_in.get("coupon_specs", False):
                    if (
                        product.id
                        not in json_product_option_in.get("coupon_specs")[
                            "applicable_product_ids"
                        ]
                    ):
                        json_product_option_in.get("coupon_specs")[
                            "applicable_product_ids"
                        ].append(product.id)
                crud.product_option.create(db, obj_in=json_product_option_in)

    product = crud.product.get(db, id=product.id)  # type: ignore
    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product


# @router.get("/{id}", response_model=schemas.Product)
# def read_product(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
#     """
#     Get product by ID.
#     """
#     product = crud.product.get(db=db, id=id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product


@router.delete("/{id}", response_model=schemas.Product)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a product.
    """
    product = validate_existing_product(
        db, product_id=id, currend_user_id=current_user.id
    )

    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, please try again after the round submission deadline",
        )

    # product = crud.product.remove(db=db, id=id)
    # product = crud.product.get(db, id=id)
    crud.product.update(
        db, db_obj=product, obj_in={"is_active": False}
    )  # todo soft deletion
    return product


@router.post("/{product_id}/artifacts/generate-upload-url")
def generate_upload_url(
    *,
    product_id: int,
    filename: str = Form(...),
    filesize: int = Form(None),
    action: str = Form(None),
    filename_suffix: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    product = crud.product.get(db, id=product_id)
    validate_new_artifact(
        product=product, current_user=current_user, url=None, filename=filename
    )

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
    artifact_in = schemas.ArtifactCreate(
        product_id=product_id,
        date=datetime.utcnow(),
        round_tournament=selling_round,
        description=description,
        url=None,
        object_name=object_name,
        object_size=filesize,
    )
    artifact = crud.artifact.create(db=db, obj_in=artifact_in)
    if not artifact:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create artifact",
        )

    # Check upload later after link expires
    celery_app.send_task(
        "app.worker.validate_artifact_upload_task",
        kwargs=dict(artifact_id=artifact.id),
        countdown=settings.ARTIFACT_UPLOAD_URL_EXPIRE_MINUTES * 60,
    )

    # Upload artifact for confirmed orders
    # orders = crud.order.get_pending_submission_orders(
    #     db, round_order=globals.selling_round  # type: ignore
    # )
    # for order in orders:
    #     print(f"Uploading csv artifact {object_name} for order {order.id}")
    #     celery_app.send_task(
    #         "app.worker.upload_numerai_artifact_task",
    #         kwargs=dict(
    #             order_id=order.id,
    #             object_name=object_name,
    #             model_id=order.submit_model_id,
    #             numerai_api_key_public_id=order.buyer.numerai_api_key_public_id,
    #             numerai_api_key_secret=order.buyer.numerai_api_key_secret,
    #             tournament=order.product.model.tournament,
    #             version=1,
    #         ),
    #         countdown=settings.ARTIFACT_UPLOAD_URL_EXPIRE_MINUTES * 60,
    #     )
    return {"id": artifact.id, "url": url}


@router.post("/{product_id}/artifacts/{artifact_id}/validate-upload")
def validate_upload(
    *,
    product_id: int,
    artifact_id: int,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    globals = crud.globals.get_singleton(db=db)
    selling_round = globals.selling_round  # type: ignore

    artifact = crud.artifact.get(db, id=artifact_id)
    artifact = validate_existing_artifact(
        artifact=artifact, product_id=product_id, selling_round=selling_round
    )

    product = crud.product.get(db, id=product_id)
    validate_new_artifact(
        product=product, current_user=current_user, url=artifact.url, filename=artifact.object_name  # type: ignore
    )

    if not artifact.object_name:
        raise HTTPException(
            status_code=400, detail="Artifact not an upload object",
        )

    blob = bucket.blob(artifact.object_name)
    if not blob.exists():
        raise HTTPException(
            status_code=404, detail="Artifact file not uploaded",
        )

    crud.artifact.update(db, db_obj=artifact, obj_in={"state": "active"})

    # mark product as ready
    if product:
        if not product.is_ready:
            crud.product.update(db, db_obj=product, obj_in={"is_ready": True})

    # validate and fulfill orders immediately
    celery_app.send_task(
        "app.worker.validate_artifact_upload_task",
        kwargs=dict(artifact_id=artifact.id, skip_if_active=False),
    )

    return artifact


@router.post("/{product_id}/artifacts", response_model=schemas.Artifact)
async def create_product_artifact(
    *,
    product_id: int,
    url: str = Body(...),
    description: str = Body(None),
    # filename: str = Body(None),
    db: Session = Depends(deps.get_db),
    # driver: StorageDriver = Depends(deps.get_cloud_storage_driver),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    product = crud.product.get(db, id=product_id)

    validate_new_artifact(
        product=product, current_user=current_user, url=url, filename=None
    )

    all_modes = [option.mode for option in product.options]  # type: ignore

    if "stake" in all_modes or "stake_with_limit" in all_modes:
        raise HTTPException(
            status_code=400,
            detail="Stake modes require native artifact uploads for automated submissions",
        )

    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, please try again after the round submission deadline",
        )

    selling_round = globals.selling_round  # type: ignore

    # Create artifact
    artifact_in = schemas.ArtifactCreate(
        product_id=product_id,
        date=datetime.utcnow(),
        round_tournament=selling_round,
        description=description,
        url=url,
        # object_name=object_name,
    )
    artifact = crud.artifact.create(db=db, obj_in=artifact_in)

    # mark product as ready
    if product:
        if not product.is_ready:
            crud.product.update(db, db_obj=product, obj_in={"is_ready": True})

    # Send notification emails
    send_artifact_emails_for_active_orders(db, artifact, is_file=False)
    return artifact


@router.put("/{product_id}/artifacts/{artifact_id}")
async def update_product_artifact(
    *,
    product_id: int,
    artifact_id: int,
    description: str = Body(None),
    url: str = Body(None),
    filename: str = Body(None),
    db: Session = Depends(deps.get_db),
    # driver: StorageDriver = Depends(deps.get_cloud_storage_driver),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    product = crud.product.get(db, id=product_id)
    validate_new_artifact(
        product=product, current_user=current_user, url=url, filename=filename
    )

    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, please try again after the round submission deadline",
        )

    selling_round = globals.selling_round  # type: ignore

    artifact = crud.artifact.get(db, id=artifact_id)
    artifact = validate_existing_artifact(
        artifact=artifact, product_id=product_id, selling_round=selling_round
    )

    # object_name = None
    # if file_obj:
    #     object_name = get_object_name(sku=product.sku, selling_round=selling_round, original_filename=file_obj.filename,
    #                                   override_filename=filename)
    #     upload_obj = upload_file(driver=driver, file_obj=file_obj, object_name=object_name)
    #     if not upload_obj:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                             detail="File could not be uploaded")

    # Update artifact
    artifact_dict = {}
    artifact_dict["description"] = description
    if url:
        artifact_dict["url"] = url
    # if file_obj:
    #     artifact_dict['object_name'] = object_name

    artifact = crud.artifact.update(db=db, db_obj=artifact, obj_in=artifact_dict)
    return artifact


@router.get(
    "/{product_id}/artifacts",
    response_model=Dict[str, Union[int, List[schemas.Artifact]]],
)
def list_product_artifacts(
    *,
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    if product.owner_id != current_user.id and not validate_buyer(
        product, current_user, selling_round
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    artifacts = crud.artifact.get_multi_by_product_round(
        db, product=product, round_tournament=selling_round
    )
    return {"total": len(artifacts), "data": artifacts}


@router.get("/{product_id}/artifacts/{artifact_id}/generate-download-url")
def generate_download_url(
    *,
    product_id: int,
    artifact_id: int,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    is_seller = product.owner_id == current_user.id
    order = validate_buyer(product, current_user, selling_round)

    # owner or buyer
    if not is_seller and not order:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # file mode
    if order and not is_seller and order.mode != "file":
        raise HTTPException(
            status_code=403, detail="Download not allowed for this artifact"
        )

    artifact = crud.artifact.get(db, id=artifact_id)
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


@router.delete("/{product_id}/artifacts/{artifact_id}", response_model=schemas.Artifact)
def delete_product_artifact(
    *,
    product_id: int,
    artifact_id: int,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an artifact.
    """
    # product ownership
    validate_existing_product(
        db, product_id=product_id, currend_user_id=current_user.id
    )

    # not during round rollover
    globals = crud.globals.get_singleton(db=db)
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, please try again after the round submission deadline",
        )

    selling_round = globals.selling_round  # type: ignore

    artifact = crud.artifact.get(db, id=artifact_id)
    validate_existing_artifact(
        artifact=artifact, product_id=product_id, selling_round=selling_round
    )

    artifact = crud.artifact.remove(db=db, id=artifact_id)
    object_name = artifact.object_name
    if object_name:
        try:
            blob = bucket.blob(object_name)
            blob.delete()
        except NotFound:
            pass
    return artifact
