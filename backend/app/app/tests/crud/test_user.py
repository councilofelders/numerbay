from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    assert user.username == email
    assert hasattr(user, "hashed_password")

    crud.user.remove(db, id=user.id)


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(db, username=email, password=password)
    assert authenticated_user
    assert user.username == authenticated_user.username

    crud.user.remove(db, id=user.id)


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.user.authenticate(db, username=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is True

    crud.user.remove(db, id=user.id)


def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, password=password, disabled=True)
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active

    crud.user.remove(db, id=user.id)


def test_check_if_user_is_superuser(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, password=password)
    user = crud.user.create(db, obj_in=user_in, is_superuser=True)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True

    crud.user.remove(db, id=user.id)


def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False

    crud.user.remove(db, id=user.id)


def test_search_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_results = crud.user.search(db, id=user.id)
    assert user_results
    assert user_results["total"] == 1
    assert user.username == user_results["data"][0].username
    assert jsonable_encoder(user) == jsonable_encoder(user_results["data"][0])

    user_results = crud.user.search(db, term=username[:5])
    assert user_results
    assert user_results["total"] > 0

    crud.user.remove(db, id=user.id)


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.username == user_2.username
    assert jsonable_encoder(user) == jsonable_encoder(user_2)

    crud.user.remove(db, id=user.id)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(username=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password)
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.username == user_2.username
    assert verify_password(new_password, user_2.hashed_password)  # type: ignore

    crud.user.remove(db, id=user.id)


def test_update_user_empty_username(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(username=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    crud.user.update(db, db_obj=user, obj_in={"username": None})
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.username == user_2.username

    crud.user.remove(db, id=user.id)
