import json
import os
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Union, Iterator
from pathlib import Path

from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, File, status, Form
from google.api_core.exceptions import NotFound
from google.cloud.storage import Bucket
from libcloud.storage.base import StorageDriver, Object
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, StreamingResponse

from app import crud, models, schemas
from app.core.config import settings
from app.api import deps

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


def validate_existing_product(db: Session, product_id: int, currend_user_id: int) -> models.Product:
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
    # todo turnkey rollout
    # if product_in.is_on_platform is not None and product_in.is_on_platform:
    #     raise HTTPException(
    #         status_code=400, detail="On-platform listing is not yet available",
    #     )

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

    # Model ownership
    model = crud.model.get_by_name(db, name=product_in.name)
    if not model:
        raise HTTPException(
            status_code=404, detail="Model not found",
        )
    if model.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not enough permissions",
        )

    # Create product
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=current_user.id, sku=sku, model_id=model.id
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
    # todo turnkey rollout
    # if product_in.is_on_platform is not None and product_in.is_on_platform:
    #     raise HTTPException(
    #         status_code=400, detail="On-platform listing is not yet available",
    #     )

    product = validate_existing_product(db, product_id=id, currend_user_id=current_user.id)

    product_in = validate_product_input(db, product_in)  # type: ignore

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
    validate_existing_product(db, product_id=id, currend_user_id=current_user.id)
    product = crud.product.remove(db=db, id=id)
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


def get_object_name(sku: str, selling_round: str, original_filename: str, override_filename: str = None):
    file_ext = Path(original_filename).suffix
    object_name = f"{sku}_{selling_round}_{uuid.uuid4().hex}"
    if override_filename:
        object_name += f"_{override_filename}"
    object_name += file_ext
    return object_name


def validate_new_artifact(product: models.Product, current_user: models.User, url: str = None,
                              filename: str = None):
    # Product exists
    if not product:
        raise HTTPException(
            status_code=404, detail=f"Product not found",
        )

    # Product ownership
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"Not enough permissions",
        )

    # Input validation
    # if not url and not filename:
    #     raise HTTPException(
    #         status_code=400, detail="You must either provide a URL or upload a file",
    #     )

    if url and filename:
        raise HTTPException(
            status_code=400, detail="You can either provide a URL or upload a file, but not both",
        )

    # todo filename suffix / desc validation

    # todo duplicate artifact


def validate_existing_artifact(artifact: models.Artifact, product_id: int, selling_round: int):
    # artifact exists
    if not artifact:
        raise HTTPException(
            status_code=404, detail=f"Artifact not found",
        )

    # artifact belongs to product
    if artifact.product_id != product_id:
        raise HTTPException(
            status_code=400, detail=f"Invalid artifact ID for product",
        )

    # artifact current round
    if artifact.round_tournament != selling_round:
        raise HTTPException(
            status_code=400, detail=f"Artifact expired",
        )


@router.post('/{product_id}/artifacts/generate-upload-url')
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
    current_user: models.User = Depends(deps.get_current_active_user)
):
    product = crud.product.get(db, id=product_id)
    validate_new_artifact(product=product, current_user=current_user, url=None, filename=filename)
    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    object_name = get_object_name(sku=product.sku, selling_round=selling_round, original_filename=filename,
                                      override_filename=filename_suffix)

    if not action:
        action = 'PUT'
    if action.upper() not in ['PUT', 'POST']:
        raise HTTPException(status_code=400, detail="Action type must be either PUT or POST for uploads")
    blob = bucket.blob(object_name)
    url = blob.generate_signed_url(
        expiration=timedelta(minutes=10),
        content_type='application/octet-stream',
        bucket_bound_hostname=('https://storage.numerbay.ai' if settings.GCP_STORAGE_BUCKET == 'storage.numerbay.ai'
                               else None),
        method=action, version="v4")

    # Create artifact
    artifact_in = schemas.ArtifactCreate(
        product_id=product_id,
        date=datetime.utcnow(),
        round_tournament=selling_round,
        description=description,
        url=None,
        object_name=object_name,
        object_size=filesize
    )
    artifact = crud.artifact.create(
        db=db, obj_in=artifact_in
    )
    if not artifact:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create artifact")
    return {'id': artifact.id, 'url': url}


@router.post('/{product_id}/artifacts', response_model=schemas.Artifact)
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
    validate_new_artifact(product=product, current_user=current_user, url=url, filename=None)

    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    # Create artifact
    artifact_in = schemas.ArtifactCreate(
        product_id=product_id,
        date=datetime.utcnow(),
        round_tournament=selling_round,
        description=description,
        url=url,
        # object_name=object_name,
    )
    artifact = crud.artifact.create(
        db=db, obj_in=artifact_in
    )
    return artifact


@router.put('/{product_id}/artifacts/{artifact_id}')
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
):
    print(description)
    product = crud.product.get(db, id=product_id)
    validate_new_artifact(product=product, current_user=current_user, url=url, filename=filename)
    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
    artifact = crud.artifact.get(db, id=artifact_id)
    validate_existing_artifact(artifact=artifact, product_id=product_id, selling_round=selling_round)

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
    artifact_dict['description'] = description
    if url:
        artifact_dict['url'] = url
    # if file_obj:
    #     artifact_dict['object_name'] = object_name

    artifact = crud.artifact.update(
        db=db, db_obj=artifact, obj_in=artifact_dict
    )
    return artifact

    # from datetime import datetime
    #
    # body = b''
    # read_first = False
    # async for chunk in file.stream():
    #     if not read_first:
    #         print(f'{datetime.now()} Read the first 100 bytes')
    #     read_first = True
    #     body += chunk
    #
    # print(f'{datetime.now()} Read all the file')

    # chunk = await file.read(100)
    # print(f'{datetime.now()} Read the first 100 bytes')
    #
    # remaining = await file.read()
    # print(f'{datetime.now()} Read all the file')


def validate_buyer(product: models.Product, current_user: models.User, selling_round: int) -> bool:
    for order in current_user.orders:
        if order.round_order == selling_round and order.product_id == product.id and order.state == 'confirmed':
            return True
    return False


@router.get('/{product_id}/artifacts', response_model=Dict[str, Union[int, List[schemas.Artifact]]])
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

    if product.owner_id != current_user.id and not validate_buyer(product, current_user, selling_round):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    artifacts = crud.artifact.get_multi_by_product_round(db, product_id=product.id, round_tournament=selling_round)
    return {'total': len(artifacts), 'data': artifacts}


@router.get('/{product_id}/artifacts/{artifact_id}/generate-download-url')
def generate_download_url(
    *,
    product_id: int,
    artifact_id: int,
    db: Session = Depends(deps.get_db),
    bucket: Bucket = Depends(deps.get_gcs_bucket),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

    if product.owner_id != current_user.id and not validate_buyer(product, current_user, selling_round):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    artifact = crud.artifact.get(db, id=artifact_id)
    if not artifact:
        raise HTTPException(status_code=404,
                            detail="Artifact not found")

    action = 'GET'
    blob = bucket.blob(artifact.object_name)
    url = blob.generate_signed_url(
        expiration=timedelta(minutes=10),
        # content_type='application/octet-stream',
        bucket_bound_hostname=('https://storage.numerbay.ai' if settings.GCP_STORAGE_BUCKET == 'storage.numerbay.ai'
                               else None),
        method=action, version="v4")
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


@router.delete('/{product_id}/artifacts/{artifact_id}', response_model=schemas.Artifact)
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
    validate_existing_product(db, product_id=product_id, currend_user_id=current_user.id)

    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
    artifact = crud.artifact.get(db, id=artifact_id)
    validate_existing_artifact(artifact=artifact, product_id=product_id, selling_round=selling_round)

    artifact = crud.artifact.remove(db=db, id=artifact_id)
    object_name = artifact.object_name
    if object_name:
        try:
            blob = bucket.blob(object_name)
            blob.delete()
        except NotFound:
            pass
    return artifact
