import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, Integer, String, Text

from src.config.database.base_table import Base


class SyncHistoryTable(Base):
    __tablename__ = "sync_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sync_type = Column(String(50))
    status = Column(String(50))
    details = Column(Text)
    duration_ms = Column(Integer)
    items_synced = Column(Integer)
    errors_count = Column(Integer)

