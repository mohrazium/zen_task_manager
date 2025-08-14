import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, String,
                        Table, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config.database.base_table import Base
from src.features.todos.data.datasource.tables.project_table import \
    ProjectTable
from src.features.todos.data.datasource.tables.task_table import TaskTable
from src.features.todos.domain.enums.status import StatusEnum
from src.features.todos.domain.enums.user_role import UserRole


class UserTable(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_settings_id = Column(UUID(as_uuid=True), ForeignKey("user_settings.id"), unique=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    github_token = Column(String(255))
    password_hash = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.user)
    status = Column(Enum(StatusEnum), default=StatusEnum.active)
    last_login = Column(DateTime)
    profile_image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    settings = relationship("UserSettingsTable",foreign_keys=[user_settings_id], uselist=False, back_populates="user")
