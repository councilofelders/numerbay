""" Database model for stats """

from sqlalchemy import JSON, Column, Integer

from app.db.base_class import Base


class Stats(Base):
    """Database model for stats"""

    id = Column(Integer, primary_key=True, index=True)
    stats = Column(JSON)
