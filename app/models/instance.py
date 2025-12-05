from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class Instance(Base):
    __tablename__ = "mc_instance"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    instance_key = Column(String(64), unique=True, nullable=False)
    host = Column(String(128))
    pid = Column(Integer)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_heartbeat = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
