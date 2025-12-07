"""
message_type.py

主要功能：消息类型定义表，包含编码、名称及启用状态。
------------------------------------------------------
作者: 团队/姓名
日期: 2025-12-06
版本: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class MessageType(Base):
    __tablename__ = "mc_message_type"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    code = Column(String(64), nullable=False, unique=True)
    name = Column(String(128), nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(BIGINT(unsigned=True))
    updated_by = Column(BIGINT(unsigned=True))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
