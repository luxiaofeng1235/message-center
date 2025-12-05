from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class Message(Base):
    __tablename__ = "mc_message"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    app_id = Column(BIGINT(unsigned=True), nullable=False)
    channel_id = Column(BIGINT(unsigned=True), nullable=False)
    message_type_id = Column(BIGINT(unsigned=True))
    message_key = Column(String(64), unique=True)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    payload = Column(JSON)
    priority = Column(Integer, default=0, nullable=False)
    status = Column(Integer, default=0, nullable=False)
    error_msg = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    published_at = Column(DateTime)
