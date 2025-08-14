import uuid

from sqlalchemy import (JSON, Boolean, Column, Date, DateTime, Enum, Float,
                        ForeignKey, String, Table, Text, Time)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config.database.base_table import Base


class TaskScheduleTable(Base):
    __tablename__ = "task_schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    start_date = Column(Date)
    due_date = Column(Date)
    recurrence_rule = Column(String(255))
    reminder_time = Column(Time)
    priority_window = Column(String(50))
    last_rescheduled_at = Column(DateTime)
    scheduling_confidence = Column(Float)

    task = relationship("TaskTable", foreign_keys=[task_id], back_populates="schedules")
