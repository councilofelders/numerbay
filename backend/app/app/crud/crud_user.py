""" CRUD for user """

import functools
from datetime import datetime
from typing import Any, Dict, Optional, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.api.dependencies import numerai
from app.core.security import get_password_hash, verify_password, verify_signature
from app.crud.base import CRUDBase
from app.models.product import Product
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD for user"""

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(self.model).filter(self.model.username == username).first()

    def get_by_public_address(
        self, db: Session, *, public_address: str
    ) -> Optional[User]:
        """Get user by public address"""
        return (
            db.query(self.model)
            .filter(self.model.public_address == public_address)
            .first()
        )

    def search(
        self,
        db: Session,
        *,
        id: int = None,  # pylint: disable=W0622
        skip: int = 0,
        limit: int = None,
        filters: Dict = None,
        term: str = None,
        sort: str = None,  # pylint: disable=W0613
    ) -> Any:
        """Search users"""
        query_filters = []
        if id is not None:
            query_filters.append(User.id == id)
        if term is not None:
            query_filters.append(
                User.username.ilike(
                    "%{}%".format(term)  # pylint: disable=consider-using-f-string
                )
            )

        if isinstance(filters, dict):
            for filter_key, _ in filters.items():
                if filter_key == "numerai_api_key_public_id":
                    query_filters.append(
                        User.numerai_api_key_public_id.is_not(None)  # type: ignore
                    )

        query = db.query(self.model)
        if len(query_filters) > 0:
            query_filter = functools.reduce(and_, query_filters)
            query = query.filter(query_filter)
        count = query.count()
        # query = query.order_by(parse_sort_option(sort))
        data = query.offset(skip).limit(limit).all()

        return {"total": count, "data": data}

    def create(  # pylint: disable=arguments-differ
        self, db: Session, *, obj_in: UserCreate, is_superuser: bool = False
    ) -> User:
        """Create user"""
        db_obj = User(  # type: ignore
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),  # type: ignore
            email=obj_in.email,
            public_address=obj_in.public_address,
            nonce=obj_in.nonce,
            is_superuser=is_superuser,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Update user"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        if "username" in update_data and not update_data["username"]:
            update_data.pop("username", None)
        if "email" in update_data and not update_data["email"]:
            update_data.pop("email", None)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        """Authenticate user"""
        user_obj = self.get_by_username(db, username=username)
        if not user_obj:
            return None
        if not verify_password(password, user_obj.hashed_password):  # type: ignore
            return None
        return user_obj

    def authenticate_web3(
        self, db: Session, *, public_address: str, signature: str
    ) -> Optional[User]:
        """Authenticate web3 user"""
        user_obj = self.get_by_public_address(db, public_address=public_address)
        if not user_obj:
            return None
        if not verify_signature(public_address, user_obj.nonce, signature):  # type: ignore
            return None
        return user_obj

    def is_active(self, user: User) -> bool:  # pylint: disable=redefined-outer-name
        """Check user active"""
        return user.is_active

    def is_superuser(self, user: User) -> bool:  # pylint: disable=redefined-outer-name
        """Check superuser"""
        return user.is_superuser

    def delist_all(self, db: Session, username: str) -> None:
        user = self.get_by_username(db, username=username)

        products_to_delist = (
            db.query(Product).filter(Product.owner_id == user.id).all()  # type: ignore
        )
        for product_obj in products_to_delist:
            product_obj.is_active = False

        db.commit()

    def update_numerai_api(self, db: Session, user_json: Dict) -> Any:
        """Update Numerai API key"""
        # Check if we already have API data (for compatibility with existing code)
        if user_json.get("_api_data"):
            api_result = user_json["_api_data"]
        else:
            # Otherwise make the API call (this maintains backward compatibility)
            api_result = numerai.get_numerai_api_info(user_json)
        
        if not api_result["success"]:
            return {"success": False, "message": api_result["message"]}
            
        user_update_json = api_result["data"]
        account = user_update_json.pop("account")  # Remove account from update data
            
        # check for duplicated numerai wallet
        duplicated_user = (
            db.query(User)
            .filter(
                and_(
                    User.id != user_json["id"],
                    User.numerai_wallet_address == account["walletAddress"],
                )
            )
            .first()
        )
        if duplicated_user is not None:
            print(
                f"Numerai API Key update failed for {user_json['username']}: "
                f"(Duplicated wallet {account['walletAddress']})"
            )
            return {"success": False, "message": "Duplicated Numerai wallet"}

        user_obj = self.get(db, user_json["id"])

        if not user_obj.email:  # type: ignore
            user_update_json["email"] = account["email"]

        # tag date of last sync
        user_update_json["date_last_numerai_sync"] = datetime.utcnow()
        self.update(db, db_obj=user_obj, obj_in=user_update_json)  # type: ignore
        return {"success": True, "message": "Numerai API Updated"}


user = CRUDUser(User)
