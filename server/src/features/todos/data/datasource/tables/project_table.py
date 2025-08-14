import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        String, Table, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config.database.base_table import Base
from src.features.todos.data.datasource.tables.task_table import TaskTable
from src.features.todos.data.datasource.tables.user_table import UserTable


class ProjectTable(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    repo_url = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    category = Column(String(50))
    status = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Float)
    progress_percentage = Column(Float)
    ai_health_score = Column(Float)

    tasks = relationship("TaskTable", foreign_keys=[owner_id], back_populates="project")