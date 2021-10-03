import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from google.api_core.exceptions import NotFound
from google.cloud.storage import Bucket
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
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
    # print(f"Product results: ({len(products)}): {products}")
    # for product in products:
    #     try:
    #         jsonable_encoder(product)
    #     except Exception:
    #         raise HTTPException(
    #             status_code=500, detail=f"Encoding failed for product {product.id}"
    #         )
    # try:
    #     jsonable_encoder(products)
    # except:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"Encoding failed for all ({len(products)}) products",
    #     )
    return products


# @router.get("/my", response_model=List[schemas.Product])
# def read_my_products(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve products.
#     """
#     products = crud.product.get_multi_by_owner(
#         db=db, owner_id=current_user.id, skip=skip, limit=limit
#     )
#     return products


def validate_product_input(
    db: Session, product_in: Union[schemas.ProductCreate, schemas.ProductUpdate]
) -> Union[schemas.ProductCreate, schemas.ProductUpdate]:
    # Positive price
    if product_in.price is not None:
        if product_in.price <= 0:
            raise HTTPException(
                status_code=400, detail="Price must be positive",
            )

    # Positive expiration round
    if product_in.expiration_round is not None:
        if product_in.expiration_round <= 0:
            raise HTTPException(
                status_code=400, detail="Expiration round must be a positive integer",
            )

        # deactivate automatically if already expired
        selling_round = crud.globals.get_singleton(db).selling_round  # type: ignore
        if product_in.expiration_round < selling_round:
            product_in.is_active = False

    # Make currency upper case
    if product_in.currency is not None:
        product_in.currency = product_in.currency.upper()

    if product_in.is_on_platform is not None:
        if product_in.is_on_platform:
            # On-platform currency type
            if product_in.currency is not None and product_in.currency not in ["NMR"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"{product_in.currency} is not supported for on-platform listing",
                )

            # On-platform decimal check
            if product_in.price is not None:
                precision = Decimal(product_in.price).as_tuple().exponent
                if precision < -4:
                    raise HTTPException(
                        status_code=400,
                        detail=f"On-platform listing price must not exceed {4} decimal places",
                    )

            # On-platform Mode check
            if product_in.mode not in ["file", "stake", "stake_with_limit"]:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid listing mode, must be one of ['file', 'stake', 'stake_with_limit']",
                )

            # On-platform Stake limit check
            if product_in.mode == "stake_with_limit":
                if product_in.stake_limit is None:
                    raise HTTPException(
                        status_code=400,
                        detail="Stake limit is required for 'stake_with_limit' mode",
                    )
                # Stake limit decimal check
                precision = Decimal(product_in.stake_limit).as_tuple().exponent
                if precision < -4:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Stake limit must not exceed {4} decimal places",
                    )

            # On-platform chain type
            if product_in.chain is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Specifying chain is not yet supported for on-platform listing",
                )
        else:
            # Off-platform currency type
            if product_in.currency is not None and product_in.currency not in ["USD"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"{product_in.currency} is not supported for off-platform listing",
                )

            # Off-platform decimal check
            if product_in.price is not None:
                precision = Decimal(product_in.price).as_tuple().exponent
                if precision < -2:
                    raise HTTPException(
                        status_code=400,
                        detail=f"On-platform listing price must not exceed {2} decimal places",
                    )

            # Off-platform chain type
            if product_in.chain is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Specifying chain is not supported for off-platform listing",
                )

    # Avatar url scheme
    if product_in.avatar and not product_in.avatar.startswith("https"):
        raise HTTPException(
            status_code=400, detail="Avatar image must be a HTTPS URL",
        )

    return product_in


def validate_existing_product(
    db: Session, product_id: int, currend_user_id: int
) -> models.Product:
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.owner_id != currend_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return product


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
    product_in = validate_product_input(db, product_in)  # type: ignore

    # Category
    category = crud.category.get(db=db, id=product_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

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
    try:
        if (
            not current_user.numerai_api_key_public_id
            or not current_user.numerai_api_key_secret
        ):
            raise ValueError
        crud.user.get_numerai_api_user_info(
            public_id=current_user.numerai_api_key_public_id,
            secret_key=current_user.numerai_api_key_secret,
        )
    except Exception:
        raise HTTPException(
            status_code=400, detail="Numerai API Error: Insufficient Permission."
        )

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

    # Create product
    product = crud.product.create_with_owner(
        db=db,
        obj_in=product_in,
        owner_id=current_user.id,
        sku=sku,
        model_id=model_id,
        tournament=tournament,
    )
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

    product_in = validate_product_input(db, product_in)  # type: ignore

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

    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product


@router.get("/{id}", response_model=schemas.Product)
def read_product(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get product by ID.
    """
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


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


# def upload_file(driver: StorageDriver, file_obj: UploadFile, object_name: str) -> Object:
#     container_name = settings.GCP_STORAGE_BUCKET
#     container = driver.get_container(container_name=container_name)
#     upload_obj = driver.upload_object_via_stream(iterator=iter(file_obj.file),
#                                                  container=container,
#                                                  object_name=object_name)
#     return upload_obj


# def download_file(driver: StorageDriver, object_name: str) -> Iterator[bytes]:
#     container_name = settings.GCP_STORAGE_BUCKET
#     container = driver.get_container(container_name=container_name)
#     obj = container.get_object(object_name)
#     download_obj = container.download_object_as_stream(obj=obj, chunk_size=1024*1024)
#     return download_obj


def get_object_name(
    sku: str, selling_round: int, original_filename: str, override_filename: str = None
) -> str:
    file_ext = Path(original_filename).suffix
    object_name = f"{sku}_{str(selling_round)}_{uuid.uuid4().hex}"
    if override_filename:
        object_name += f"_{override_filename}"
    object_name += file_ext
    return object_name


def validate_new_artifact(
    product: Optional[models.Product],
    current_user: models.User,
    url: str = None,
    filename: str = None,
) -> None:
    # Product exists
    if not product:
        raise HTTPException(
            status_code=404, detail="Product not found",
        )

    # Product ownership
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not enough permissions",
        )

    # Input validation
    # if not url and not filename:
    #     raise HTTPException(
    #         status_code=400, detail="You must either provide a URL or upload a file",
    #     )

    if url and filename:
        raise HTTPException(
            status_code=400,
            detail="You can either provide a URL or upload a file, but not both",
        )

    if url and not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(
            status_code=400, detail="Invalid URL",
        )

    # todo filename suffix / desc validation

    # todo duplicate artifact


def validate_existing_artifact(
    artifact: Optional[models.Artifact], product_id: int, selling_round: int
) -> models.Artifact:
    # artifact exists
    if not artifact:
        raise HTTPException(
            status_code=404, detail="Artifact not found",
        )

    # artifact belongs to product
    if artifact.product_id != product_id:
        raise HTTPException(
            status_code=400, detail="Invalid artifact ID for product",
        )

    # artifact current round
    if (
        artifact.product.category.is_per_round  # type: ignore
        and artifact.round_tournament < selling_round  # type: ignore
    ):
        raise HTTPException(
            status_code=400, detail="Artifact expired",
        )
    return artifact


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

    # Upload artifact for confirmed orders
    orders = crud.order.get_pending_submission_orders(
        db, round_order=globals.selling_round  # type: ignore
    )
    for order in orders:
        print(f"Uploading csv artifact {object_name} for order {order.id}")
        celery_app.send_task(
            "app.worker.upload_numerai_artifact_task",
            kwargs=dict(
                order_id=order.id,
                object_name=object_name,
                model_id=order.submit_model_id,
                numerai_api_key_public_id=order.buyer.numerai_api_key_public_id,
                numerai_api_key_secret=order.buyer.numerai_api_key_secret,
                tournament=order.product.model.tournament,
                version=1,
            ),
            countdown=settings.ARTIFACT_UPLOAD_URL_EXPIRE_MINUTES * 60,
        )
    return {"id": artifact.id, "url": url}


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


def validate_buyer(
    product: models.Product, current_user: models.User, selling_round: int
) -> Optional[models.Order]:
    for order in current_user.orders:  # type: ignore
        if (
            order.round_order == selling_round
            and order.product_id == product.id
            and order.state == "confirmed"
        ):
            return order
    return None


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


# @router.get('/{product_id}/artifacts/{artifact_id}')
# def download_product_artifact(
#     *,
#     product_id: int,
#     artifact_id: int,
#     db: Session = Depends(deps.get_db),
#     driver: StorageDriver = Depends(deps.get_cloud_storage_driver),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     # product ownership
#     validate_existing_product(db, product_id=product_id, currend_user_id=current_user.id)
#
#     selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
#     artifact = crud.artifact.get(db, id=artifact_id)
#     validate_existing_artifact(artifact=artifact, product_id=product_id, selling_round=selling_round)
#
#     if artifact.object_name:
#         download_obj = download_file(driver, object_name=artifact.object_name)
#         return StreamingResponse(download_obj)
#     else:
#         return artifact


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
