"""
client_connection.py

主要功能：记录 WebSocket 客户端连接状态（在线/活跃/下线）及接入信息。
------------------------------------------------------
作者: 团队/姓名
日期: 2025-12-06
版本: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class ClientConnection(Base):
    __tablename__ = "mc_client_connection"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(unsigned=True), nullable=False)
    instance_id = Column(BIGINT(unsigned=True), nullable=False)
    client_id = Column(String(128))
    role = Column(String(32))
    token = Column(String(255))
    user_agent = Column(String(255))
    ip = Column(String(45))
    connected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_active_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    disconnected_at = Column(DateTime)
