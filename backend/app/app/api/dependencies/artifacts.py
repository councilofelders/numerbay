""" Dependencies for artifacts endpoints """

from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.core.config import settings
from app.utils import send_new_artifact_email, send_new_artifact_seller_email


def validate_new_artifact(
    product: Optional[models.Product],
    current_user: models.User,
    url: str = None,
    filename: str = None,
) -> None:
    """Validate new artifacts"""
    # Product exists
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    # Product ownership
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
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
            status_code=400,
            detail="Invalid URL",
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
    """Validate existing artifact"""
    # artifact exists
    if not artifact:
        raise HTTPException(
            status_code=404,
            detail="Artifact not found",
        )

    # artifact belongs to product
    if artifact.product_id != product_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid artifact ID for product",
        )

    # artifact current round
    if (
        artifact.product.category.is_per_round  # type: ignore
        and artifact.round_tournament < selling_round  # type: ignore
    ):
        raise HTTPException(
            status_code=400,
            detail="Artifact expired",
        )
    return artifact


def send_artifact_emails_for_active_orders(
    db: Session, artifact: models.Artifact, is_file: bool = True
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
                        artifact=artifact.object_name if is_file else artifact.url,  # type: ignore
                    )

        # Send new artifact email notification to seller
        if artifact.product.owner.email:
            send_new_artifact_seller_email(
                email_to=artifact.product.owner.email,
                username=artifact.product.owner.username,
                round_tournament=artifact.round_tournament,  # type: ignore
                product=artifact.product.sku,
                artifact=artifact.object_name if is_file else artifact.url,  # type: ignore
            )
