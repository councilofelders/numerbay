import functools
from typing import Any, Dict, Optional, Union

from numerapi import NumerAPI
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password, verify_signature
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_public_address(
        self, db: Session, *, public_address: str
    ) -> Optional[User]:
        return db.query(User).filter(User.public_address == public_address).first()

    def search(
        self,
        db: Session,
        *,
        id: int = None,
        skip: int = 0,
        limit: int = 100,
        filters: Dict = None,
        term: str = None,
        sort: str = None
    ) -> Any:
        query_filters = []
        if id is not None:
            query_filters.append(User.id == id)
        if term is not None:
            query_filters.append(User.username.like("%{}%".format(term)))

        if isinstance(filters, dict):
            for filter_key, filter_item in filters.items():
                if filter_key == "numerai_api_key_public_id":
                    query_filters.append(User.numerai_api_key_public_id.is_not(None))  # type: ignore

        query = db.query(self.model)
        if len(query_filters) > 0:
            query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
            query = query.filter(query_filter)
        count = query.count()
        # query = query.order_by(parse_sort_option(sort))
        data = query.offset(skip).limit(limit).all()

        return {"total": count, "data": data}

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(  # type: ignore
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),  # type: ignore
            email=obj_in.email,
            public_address=obj_in.public_address,
            nonce=obj_in.nonce,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        if "username" in update_data and not update_data["username"]:
            update_data["username"] = None
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):  # type: ignore
            return None
        return user

    def authenticate_web3(
        self, db: Session, *, public_address: str, signature: str
    ) -> Optional[User]:
        user = self.get_by_public_address(db, public_address=public_address)
        if not user:
            return None
        if not verify_signature(public_address, user.nonce, signature):  # type: ignore
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def get_numerai_api_user_info(self, public_id: str, secret_key: str):
        """
        Retrieve numerai user info.
        """
        query = """
                  query {
                    account {
                      username
                      email
                      id
                      status
                      insertedAt
                      walletAddress
                      apiTokens {
                        name
                        publicId
                        scopes
                      }
                    }
                  }
                """

        api = NumerAPI(public_id=public_id, secret_key=secret_key)
        account = api.raw_query(query, authorization=True)["data"]["account"]
        return account

    def update_numerai_api(self, db: Session, user_json: Dict) -> bool:
        if (
            "numerai_api_key_secret" not in user_json
            or user_json["numerai_api_key_secret"] is None
            or user_json["numerai_api_key_secret"] == ""
        ):
            print(f"Update failed user (API Key): {user_json['username']}")
            return False
        try:
            account = self.get_numerai_api_user_info(
                public_id=user_json.get("numerai_api_key_public_id", None),
                secret_key=user_json.get("numerai_api_key_secret"),  # type: ignore
            )  # type: ignore

            api_key = list(filter(lambda token: token['publicId'] == user_json.get("numerai_api_key_public_id"),
                                  account['apiTokens']))
            if len(api_key) < 1:
                print(f"Update failed user (API Key): {user_json['username']}")
                return False

            api_scopes = api_key[0]['scopes']

            user_update_json = {
                'numerai_api_key_can_upload_submission': 'upload_submission' in api_scopes,
                'numerai_api_key_can_stake': 'stake' in api_scopes,
                'numerai_api_key_can_read_submission_info': 'read_submission_info' in api_scopes,
                'numerai_api_key_can_read_user_info': 'read_user_info' in api_scopes,
                'numerai_wallet_address': account['walletAddress']
            }

            user = self.get(db, user_json['id'])
            self.update(db, db_obj=user, obj_in=user_update_json)
            return True
        except Exception as e:
            print(f"Update failed user (Exception): {user_json['username']}: {e}")
            return False


user = CRUDUser(User)
