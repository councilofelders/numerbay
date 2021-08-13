from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship, backref

from app.db.base_class import Base


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('category.id'))
    items = relationship("Category", lazy="joined", backref=backref('parent', remote_side=[id]))