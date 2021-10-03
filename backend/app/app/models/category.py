from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from app.db.base_class import Base


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, index=True)
    tournament = Column(Integer, nullable=True, index=True)
    is_per_round = Column(Boolean, server_default="t")
    parent_id = Column(Integer, ForeignKey("category.id"))
    items = relationship(
        "Category", lazy="joined", backref=backref("parent", remote_side=[id])
    )
