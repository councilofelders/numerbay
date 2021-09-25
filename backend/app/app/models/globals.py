from sqlalchemy import Boolean, Column, Integer

from app.db.base_class import Base


class Globals(Base):
    id = Column(Integer, primary_key=True, index=True)
    active_round = Column(Integer, primary_key=True, index=True)
    selling_round = Column(Integer, primary_key=True, index=True)
    is_doing_round_rollover = Column(
        Boolean, nullable=False, default=False, server_default="f"
    )
