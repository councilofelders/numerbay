from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Globals(Base):
    id = Column(Integer, primary_key=True, index=True)
    active_round = Column(Integer, primary_key=True, index=True)
    selling_round = Column(Integer, primary_key=True, index=True)

