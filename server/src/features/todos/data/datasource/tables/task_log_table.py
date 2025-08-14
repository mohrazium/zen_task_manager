import uuid

from sqlalchemy import (JSON, UUID, Boolean, Column, Date, DateTime, Enum,
                        Float, ForeignKey, Integer, String, Table, Text, Time)
from sqlalchemy.orm import declarative_base, relationship

from src.config.database.base_table import Base


class TaskLogTable(Base):
    __tablename__ = "task_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    date = Column(Date)
    progress_percentage = Column(Float)
    notes = Column(Text)
    time_spent = Column(Float)  # hours
    mood_score = Column(Integer)
    energy_level = Column(Integer)
    obstacles = Column(Text)

    task = relationship("TaskTable", foreign_keys=[task_id], back_populates="logs")
