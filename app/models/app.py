from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Integer, JSON
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class App(Base):
    __tablename__ = "mc_app"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    code = Column(String(64), unique=True, nullable=False)
    secret = Column(String(128), nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    mode = Column(Integer, default=0, nullable=False)
    mode_config = Column(JSON)
    created_by = Column(BIGINT(unsigned=True))
    updated_by = Column(BIGINT(unsigned=True))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
