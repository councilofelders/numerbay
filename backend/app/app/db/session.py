from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import functools
from typing import Callable

from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_size=15,
    max_overflow=20,
    pool_timeout=60,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def with_db_session(func: Callable):
    """Execute a function with a database session and ensure it's closed properly."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            return func(db, *args, **kwargs)
        finally:
            db.close()
    return wrapper
