from sqlalchemy.orm import Session

from app import crud, models, schemas


def create_model_for_product(
    db: Session, product_name: str, owner_id: int
) -> models.Model:
    model = crud.model.create(
        db,
        obj_in=schemas.ModelCreate(
            id=product_name,
            name=product_name,
            tournament=8,
            owner_id=owner_id,
        ),
    )
    return model
