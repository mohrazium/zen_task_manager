import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class AISuggestion(Base):
    __tablename__ = "ai_suggestions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    suggestion_text = Column(Text)
    acceptance_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    suggestion_type = Column(String(50))
    source = Column(String(50))
    ai_confidence = Column(Float)
    applied_at = Column(DateTime)

    task = relationship("TaskTable", foreign_keys=[task_id], back_populates="ai_suggestions")
