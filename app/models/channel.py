from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, JSON, String, Integer
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class Channel(Base):
    __tablename__ = "mc_channel"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    app_id = Column(BIGINT(unsigned=True), nullable=False)
    channel_key = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    dispatch_mode = Column(Integer, default=0, nullable=False)
    broadcast_filter = Column(JSON)
    created_by = Column(BIGINT(unsigned=True))
    updated_by = Column(BIGINT(unsigned=True))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
