import re
from decimal import Decimal
from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas


def validate_product_input(
    db: Session,
    product_in: Union[schemas.ProductCreate, schemas.ProductUpdate],
    category: Union[schemas.Category, models.Category],
    current_user: Union[schemas.User, models.User],
) -> Union[schemas.ProductCreate, schemas.ProductUpdate]:
    # Product name
    if isinstance(product_in, schemas.ProductCreate) and re.match(r"^[\w-]+$", product_in.name) is None:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Invalid product name (should only contain alphabetic characters, numbers, dashes or underscores)",
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

    # Avatar url scheme
    if product_in.avatar and not product_in.avatar.startswith("https"):
        raise HTTPException(
            status_code=400, detail="Avatar image must be a HTTPS URL",
        )

    # todo options validation

    # At least one option
    if (
        isinstance(product_in, schemas.ProductCreate)
        and (product_in.options is None or len(product_in.options) == 0)
    ) or (
        isinstance(product_in, schemas.ProductUpdate)
        and product_in.options is not None
        and len(product_in.options) == 0
    ):
        raise HTTPException(
            status_code=400, detail="At least one pricing option is required",
        )

    # On-platform pricing options
    if product_in.options is not None and len(product_in.options) > 0:
        options_set = set()
        for product_option in product_in.options:
            option_tuple = (
                product_option.is_on_platform,
                product_option.price,
                product_option.currency,
            )
            option_exists = option_tuple in options_set
            options_set.add(option_tuple)

            if option_exists:
                raise HTTPException(
                    status_code=400, detail="Duplicated pricing not allowed",
                )

            # Positive price
            if product_option.price is not None:
                if product_option.price <= 0:
                    raise HTTPException(
                        status_code=400, detail="Price must be positive",
                    )

            # Positive quantity
            if product_option.quantity is not None:
                if product_option.quantity <= 0:
                    raise HTTPException(
                        status_code=400, detail="Quantity must be positive",
                    )

            # Make currency upper case
            if product_option.currency is not None:
                product_option.currency = product_option.currency.upper()

            if product_option.is_on_platform:
                # On-platform currency type
                if (
                    product_option.currency is not None
                    and product_option.currency not in ["NMR"]
                ):
                    raise HTTPException(
                        status_code=400,
                        detail=f"{product_option.currency} is not supported for on-platform listing",
                    )

                # On-platform decimal check
                if product_option.price is not None:
                    precision = Decimal(product_option.price).as_tuple().exponent
                    if precision < -4:
                        raise HTTPException(
                            status_code=400,
                            detail=f"On-platform listing price must not exceed {4} decimal places",
                        )

                    # On-platform amount check
                    if product_option.currency == "NMR" and product_option.price < 1:
                        raise HTTPException(
                            status_code=400,
                            detail="On-platform listing price must be greater than 1 NMR",
                        )

                # On-platform Mode check
                if product_option.mode not in ["file", "stake", "stake_with_limit"]:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid listing mode, must be one of ['file', 'stake', 'stake_with_limit']",
                    )

                # On-platform Stake limit check
                if product_option.mode == "stake_with_limit":
                    if product_option.stake_limit is None:
                        raise HTTPException(
                            status_code=400,
                            detail="Stake limit is required for 'stake_with_limit' mode",
                        )
                    # Stake limit decimal check
                    precision = Decimal(product_option.stake_limit).as_tuple().exponent
                    if precision < -4:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Stake limit must not exceed {4} decimal places",
                        )
                    # Stake limit amount check
                    if product_option.stake_limit < 1:
                        raise HTTPException(
                            status_code=400,
                            detail="Stake limit must be greater than 1 NMR",
                        )

                # On-platform chain type
                if product_option.chain is not None:
                    raise HTTPException(
                        status_code=400,
                        detail="Specifying chain is not yet supported for on-platform listing",
                    )

                # On-platform coupon and specs
                if product_option.coupon:
                    # require specs
                    if not product_option.coupon_specs or not isinstance(
                        product_option.coupon_specs, dict
                    ):
                        raise HTTPException(
                            status_code=400, detail="Coupon specs must be provided",
                        )

                    # drop unknown fields
                    product_option.coupon_specs = {
                        k: v
                        for k, v in product_option.coupon_specs.items()
                        if k
                        in [
                            "reward_min_spend",
                            "applicable_product_ids",
                            "discount_percent",
                            "max_discount",
                            "min_spend",
                        ]
                    }

                    if "applicable_product_ids" not in product_option.coupon_specs.keys() or not isinstance(
                        product_option.coupon_specs["applicable_product_ids"], list
                    ):
                        raise HTTPException(
                            status_code=400,
                            detail="List of applicable product IDs must be provided in coupon specs",
                        )

                    if "discount_percent" not in product_option.coupon_specs.keys():
                        raise HTTPException(
                            status_code=400,
                            detail="Discount percentage (0-100) must be provided in coupon specs",
                        )

                    if "max_discount" not in product_option.coupon_specs.keys():
                        raise HTTPException(
                            status_code=400,
                            detail="Max discount (in NMR) must be provided in coupon specs",
                        )

                    # validate specs
                    if "reward_min_spend" in product_option.coupon_specs.keys() and not (
                        Decimal(product_option.coupon_specs["reward_min_spend"])
                        >= Decimal("1")
                    ):
                        raise HTTPException(
                            status_code=400,
                            detail="Min spend (in NMR) for rewarding coupon must be above 1",
                        )

                    for applicable_product_id in product_option.coupon_specs[
                        "applicable_product_ids"
                    ]:
                        applicable_product_obj = crud.product.get(
                            db, id=applicable_product_id
                        )
                        if (
                            not applicable_product_obj
                            or applicable_product_obj.owner_id != current_user.id
                        ):
                            raise HTTPException(
                                status_code=400,
                                detail=f"Invalid applicable product ID {applicable_product_id}",
                            )

                    if (
                        not isinstance(
                            product_option.coupon_specs["discount_percent"], int
                        )
                        or product_option.coupon_specs["discount_percent"] > 100
                        or product_option.coupon_specs["discount_percent"] < 0
                    ):
                        raise HTTPException(
                            status_code=400,
                            detail="Discount percentage must be an integer between 0-100",
                        )

                    if Decimal(product_option.coupon_specs["max_discount"]) <= Decimal(
                        "0"
                    ):
                        raise HTTPException(
                            status_code=400, detail="Max discount must be positive",
                        )

                    if "min_spend" in product_option.coupon_specs.keys() and Decimal(
                        product_option.coupon_specs["min_spend"]
                    ) < Decimal("1"):
                        raise HTTPException(
                            status_code=400, detail="Coupon min spend must be above 1",
                        )
            else:
                # Off-platform currency type
                if (
                    product_option.currency is not None
                    and product_option.currency not in ["USD"]
                ):
                    raise HTTPException(
                        status_code=400,
                        detail=f"{product_option.currency} is not supported for off-platform listing",
                    )

                # Off-platform decimal check
                if product_option.price is not None:
                    precision = Decimal(product_option.price).as_tuple().exponent
                    if precision < -2:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Off-platform listing price must not exceed {2} decimal places",
                        )

                # Off-platform chain type
                if product_option.chain is not None:
                    raise HTTPException(
                        status_code=400,
                        detail="Specifying chain is not supported for off-platform listing",
                    )

                # Off-platform coupon and specs
                if product_option.coupon or product_option.coupon_specs:
                    raise HTTPException(
                        status_code=400,
                        detail="Rewarding coupon is not supported for off-platform listing",
                    )

    # Category
    for product_option_in in product_in.options:  # type: ignore
        # On-platform Category Mode check
        if (
            product_option_in.is_on_platform
            and product_option_in.mode in ["stake", "stake_with_limit"]
            and not category.is_submission
        ):
            raise HTTPException(
                status_code=400,
                detail="Stake modes are not allowed for non-submission categories",
            )

        # On-platform Category Quantity check
        if (
            not category.is_per_round
            and product_option_in.quantity is not None
            and product_option_in.quantity > 1
        ):
            raise HTTPException(
                status_code=400,
                detail="This product is not per-round, quantity must be 1",
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


def validate_buyer(
    product: models.Product, current_user: models.User, selling_round: int
) -> Optional[models.Order]:
    for order in current_user.orders:  # type: ignore
        if (
            order.round_order > selling_round - order.quantity
            and order.product_id == product.id
            and order.state == "confirmed"
        ):
            return order
    return None
