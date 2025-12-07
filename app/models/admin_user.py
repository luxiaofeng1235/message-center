"""
admin_user.py

主要功能：定义后台管理员账户模型，包含登录信息和状态标记。
------------------------------------------------------
作者: 团队/姓名
日期: 2025-12-06
版本: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class AdminUser(Base):
    __tablename__ = "mc_admin_user"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    avatar = Column(String(255))
    display_name = Column(String(128))
    phone = Column(String(32))
    is_super = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login_ip = Column(String(45))
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
