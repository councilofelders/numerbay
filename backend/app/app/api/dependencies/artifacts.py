import uuid
from pathlib import Path
from typing import Optional

from fastapi import HTTPException

from app import models


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

    # todo test

    # At least one on-platform option
    has_on_platform = False
    for option in product.options:  # type: ignore
        if option.is_on_platform:
            has_on_platform = True
            break
    if not has_on_platform:
        raise HTTPException(
            status_code=400,
            detail="At least one on-platform pricing option is required",
        )


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
