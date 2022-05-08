""" Database model for category """

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from app.db.base_class import Base


class Category(Base):
    """Database model for category"""

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, index=True)
    tournament = Column(Integer, nullable=True, index=True)
    is_per_round = Column(Boolean, server_default="t")
    is_submission = Column(Boolean, server_default="f")
    is_per_model = Column(Boolean, server_default="f")
    parent_id = Column(Integer, ForeignKey("category.id"))
    items = relationship(
        "Category", lazy="joined", backref=backref("parent", remote_side=[id])
    )
