from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class Subscription(Base):
    __tablename__ = "mc_subscription"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(unsigned=True), nullable=False)
    channel_id = Column(BIGINT(unsigned=True), nullable=False)
    message_type_id = Column(BIGINT(unsigned=True))
    is_active = Column(Boolean, default=True, nullable=False)
    source = Column(Integer, default=1, nullable=False)
    created_by = Column(BIGINT(unsigned=True))
    updated_by = Column(BIGINT(unsigned=True))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
