from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, JSON, String, Text
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class MessageTemplate(Base):
    __tablename__ = "mc_message_template"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    app_id = Column(BIGINT(unsigned=True), nullable=False)
    channel_id = Column(BIGINT(unsigned=True))
    template_key = Column(String(64), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    title_template = Column(String(255))
    content_template = Column(Text, nullable=False)
    payload_template = Column(JSON)
    is_default = Column(Boolean, default=False, nullable=False)
    created_by = Column(BIGINT(unsigned=True))
    updated_by = Column(BIGINT(unsigned=True))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
