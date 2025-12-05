from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.mysql import BIGINT

from app.db.base import Base


class MessageDelivery(Base):
    __tablename__ = "mc_message_delivery"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    message_id = Column(BIGINT(unsigned=True), nullable=False)
    user_id = Column(BIGINT(unsigned=True), nullable=False)
    instance_id = Column(BIGINT(unsigned=True))
    client_connection_id = Column(BIGINT(unsigned=True))
    status = Column(Integer, default=0, nullable=False)
    retry_count = Column(Integer, default=0, nullable=False)
    last_error = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sent_at = Column(DateTime)
    ack_at = Column(DateTime)
