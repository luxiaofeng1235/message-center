"""
message.py

主要功能：消息主表，记录消息体、派发模式、优先级与时间戳。
------------------------------------------------------
作者: 团队/姓名
日期: 2025-12-06
版本: 1.0.0
"""

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
    sender_user_id = Column(String(128))
    priority = Column(Integer, default=0, nullable=False)
    dispatch_mode = Column(Integer, default=0, nullable=False)
    target_user_ids = Column(JSON)
    status = Column(Integer, default=0, nullable=False)
    error_msg = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    published_at = Column(DateTime)
