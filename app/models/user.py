from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class User(Base):
    __tablename__ = "mc_user"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    app_id = Column(BIGINT(unsigned=True), nullable=False)
    external_user_id = Column(String(128), nullable=False)
    nickname = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
