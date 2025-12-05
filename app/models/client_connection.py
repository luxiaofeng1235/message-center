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
    user_agent = Column(String(255))
    ip = Column(String(45))
    connected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    disconnected_at = Column(DateTime)
