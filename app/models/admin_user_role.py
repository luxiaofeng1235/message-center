from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class AdminUserRole(Base):
    __tablename__ = "mc_admin_user_role"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(unsigned=True), nullable=False)
    role_id = Column(BIGINT(unsigned=True), nullable=False)
