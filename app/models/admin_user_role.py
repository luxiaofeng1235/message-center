"""
admin_user_role.py

主要功能：后台用户与角色的关联关系模型。
------------------------------------------------------
作者: 团队/姓名
日期: 2025-12-06
版本: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class AdminUserRole(Base):
    __tablename__ = "mc_admin_user_role"
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(unsigned=True), nullable=False)
    role_id = Column(BIGINT(unsigned=True), nullable=False)
    created_at = Column(DateTime(True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(True), default=datetime.utcnow(),onupdate=datetime.utcnow(), nullable=False)
