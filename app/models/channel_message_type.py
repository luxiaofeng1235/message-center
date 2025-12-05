from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, JSON
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class ChannelMessageType(Base):
    __tablename__ = "mc_channel_message_type"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    channel_id = Column(BIGINT(unsigned=True), nullable=False)
    message_type_id = Column(BIGINT(unsigned=True), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    config = Column(JSON)
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(BIGINT(unsigned=True))
    updated_by = Column(BIGINT(unsigned=True))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
