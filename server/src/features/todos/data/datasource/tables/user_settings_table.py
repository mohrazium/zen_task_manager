import enum
import uuid
from datetime import datetime

from sqlalchemy import (JSON, UUID, Boolean, Column, Date, DateTime, Enum,
                        Float, ForeignKey, Integer, String, Table, Text, Time)
from sqlalchemy.orm import declarative_base, relationship

from src.config.database.base_table import Base


class UserSettingsTable(Base):
    __tablename__ = "user_settings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    obsidian_vault_path = Column(String(255))
    work_hours_per_day = Column(Integer)
    timezone = Column(String(50))
    preferred_language = Column(String(50))
    notification_preferences = Column(JSON)
    theme = Column(String(50))
    default_view = Column(String(50))
    auto_sync_enabled = Column(Boolean, default=True)
    weekly_goal_hours = Column(Integer)

    user = relationship("UserTable", foreign_keys=[user_id], back_populates="settings")
