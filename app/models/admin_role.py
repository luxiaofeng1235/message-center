"""
admin_role.py

主要功能：定义后台角色模型，记录角色名称与描述。
------------------------------------------------------
作者: 团队/姓名
日期: 2025-12-06
版本: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class AdminRole(Base):
    __tablename__ = "mc_admin_role"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    code = Column(String(64), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
