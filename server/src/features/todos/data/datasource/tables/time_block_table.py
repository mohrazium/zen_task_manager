import uuid

from sqlalchemy import (UUID, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class TimeBlockTable(Base):
    __tablename__ = "time_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    scheduled_start = Column(DateTime)
    scheduled_end = Column(DateTime)
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)
    focus_score = Column(Float)
    interruptions = Column(Integer)
    location = Column(String(255))
    device_used = Column(String(100))

    task = relationship("TaskTable", foreign_keys=[task_id], back_populates="time_blocks")