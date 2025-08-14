import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (JSON, Boolean, Column, Date, DateTime, Enum, Float,
                        ForeignKey, String, Table, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config.database.base_table import Base
from src.features.todos.data.datasource.tables.project_table import \
    ProjectTable
from src.features.todos.data.datasource.tables.user_table import UserTable
from src.features.todos.domain.enums.priority import PriorityEnum


class TaskTable(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50))
    priority = Column(Enum(PriorityEnum))
    type = Column(String(50))
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    parent_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    markdown_file_id = Column(UUID(as_uuid=True), ForeignKey("markdown_files.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    labels = Column(JSON)
    dependencies = Column(JSON)
    progress_percentage = Column(Float)
    effort_level = Column(String(50))
    due_date = Column(Date)
    completed_at = Column(DateTime)
    ai_priority_score = Column(Float)
    blocked_reason = Column(Text)

    project = relationship("Project", foreign_keys=[project_id], back_populates="tasks")
