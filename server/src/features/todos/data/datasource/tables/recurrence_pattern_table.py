import enum
import uuid

from sqlalchemy import (JSON, UUID, Boolean, Column, Date, DateTime, Enum,
                        Float, ForeignKey, Integer, String, Table, Text, Time)
from sqlalchemy.orm import declarative_base, relationship

from src.config.database.base_table import Base


class RecurrencePatternTable(Base):
    __tablename__ = "recurrence_patterns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    daily = Column(Boolean, default=False)
    weekly = Column(Boolean, default=False)
    monthly = Column(Boolean, default=False)
    yearly = Column(Boolean, default=False)
    custom_cron = Column(String(255))
    exceptions = Column(JSON)  # list of dates to skip
    end_date = Column(Date)
