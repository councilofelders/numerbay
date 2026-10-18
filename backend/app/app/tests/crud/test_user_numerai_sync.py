from typing import Any, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def _api_data(email: str) -> Dict[str, Any]:
    wallet = "0x" + "ab" * 20
    return {
        "success": True,
        "message": "",
        "data": {
            "numerai_api_key_can_upload_submission": True,
            "numerai_api_key_can_stake": True,
            "numerai_api_key_can_read_submission_info": True,
            "numerai_api_key_can_read_user_info": True,
            "numerai_wallet_address": wallet,
            "account": {"email": email, "walletAddress": wallet},
        },
    }


def _create_user(db: Session) -> Any:
    user_in = UserCreate(username=random_email(), password=random_lower_string())
    return crud.user.create(db, obj_in=user_in)


def test_sync_adopts_email_when_none(db: Session) -> None:
    user = _create_user(db)
    numerai_email = random_email()
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(numerai_email)

    result = crud.user.update_numerai_api(db, user_json)
    assert result["success"] is True

    db.expire_all()
    updated = crud.user.get(db, id=user.id)
    assert updated.email == numerai_email
    assert updated.email_verified is False

    crud.user.remove(db, id=user.id)


def test_sync_flag_on_adopts_unverified(db: Session, monkeypatch) -> None:
    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", True)
    local_email = random_email()
    user = _create_user(db)
    crud.user.update(db, db_obj=user, obj_in={"email": local_email})

    numerai_email = random_email()
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(numerai_email)

    result = crud.user.update_numerai_api(db, user_json)
    assert result["success"] is True

    db.expire_all()
    updated = crud.user.get(db, id=user.id)
    assert updated.email == numerai_email
    assert updated.email_verified is False

    crud.user.remove(db, id=user.id)


def test_sync_flag_on_keeps_verified(db: Session, monkeypatch) -> None:
    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", True)
    local_email = random_email()
    user = _create_user(db)
    crud.user.update(
        db, db_obj=user, obj_in={"email": local_email, "email_verified": True}
    )

    numerai_email = random_email()
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(numerai_email)

    result = crud.user.update_numerai_api(db, user_json)
    assert result["success"] is True

    db.expire_all()
    updated = crud.user.get(db, id=user.id)
    assert updated.email == local_email
    assert updated.email_verified is True

    crud.user.remove(db, id=user.id)


def test_sync_flag_on_follows_numerai_email_change(db: Session, monkeypatch) -> None:
    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", True)
    user = _create_user(db)
    first_email = random_email()
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(first_email)

    assert crud.user.update_numerai_api(db, user_json)["success"] is True
    db.expire_all()
    assert crud.user.get(db, id=user.id).email == first_email

    second_email = random_email()
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(second_email)

    assert crud.user.update_numerai_api(db, user_json)["success"] is True
    db.expire_all()
    updated = crud.user.get(db, id=user.id)
    assert updated.email == second_email
    assert updated.email_verified is False

    crud.user.remove(db, id=user.id)


def test_sync_flag_off_keeps_existing_email(db: Session) -> None:
    local_email = random_email()
    user = _create_user(db)
    crud.user.update(db, db_obj=user, obj_in={"email": local_email})

    numerai_email = random_email()
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(numerai_email)

    result = crud.user.update_numerai_api(db, user_json)
    assert result["success"] is True

    db.expire_all()
    updated = crud.user.get(db, id=user.id)
    assert updated.email == local_email

    crud.user.remove(db, id=user.id)


def test_sync_preserves_pending_when_unchanged(db: Session, monkeypatch) -> None:
    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", True)
    user = _create_user(db)
    adopted_email = random_email()
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(adopted_email)

    assert crud.user.update_numerai_api(db, user_json)["success"] is True
    db.expire_all()

    pending_email = random_email()
    crud.user.update(
        db,
        db_obj=crud.user.get(db, id=user.id),
        obj_in={"pending_email": pending_email},
    )

    user_json = jsonable_encoder(crud.user.get(db, id=user.id))
    user_json["_api_data"] = _api_data(adopted_email)

    assert crud.user.update_numerai_api(db, user_json)["success"] is True
    db.expire_all()
    updated = crud.user.get(db, id=user.id)
    assert updated.email == adopted_email
    assert updated.pending_email == pending_email

    crud.user.remove(db, id=user.id)


def test_sync_email_conflict(db: Session) -> None:
    other = _create_user(db)
    conflict_email = random_email()
    crud.user.update(db, db_obj=other, obj_in={"email": conflict_email})

    user = _create_user(db)
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(conflict_email)

    result = crud.user.update_numerai_api(db, user_json)
    assert result["success"] is False
    assert result["message"] == "Duplicated email"

    db.expire_all()
    updated = crud.user.get(db, id=user.id)
    assert updated.email is None

    crud.user.remove(db, id=user.id)
    crud.user.remove(db, id=other.id)


def test_sync_clears_pending_email(db: Session, monkeypatch) -> None:
    monkeypatch.setattr(settings, "REQUIRE_EMAIL_VERIFICATION", True)
    user = _create_user(db)
    old_email = random_email()
    pending_email = random_email()
    crud.user.update(
        db, db_obj=user, obj_in={"email": old_email, "pending_email": pending_email}
    )

    numerai_email = random_email()
    user_json = jsonable_encoder(user)
    user_json["_api_data"] = _api_data(numerai_email)

    result = crud.user.update_numerai_api(db, user_json)
    assert result["success"] is True

    db.expire_all()
    updated = crud.user.get(db, id=user.id)
    assert updated.email == numerai_email
    assert updated.pending_email is None
    assert updated.email_verified is False

    crud.user.remove(db, id=user.id)
