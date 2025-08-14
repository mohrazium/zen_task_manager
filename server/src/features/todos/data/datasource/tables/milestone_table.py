import uuid

from sqlalchemy import (UUID, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, Text)
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class MilestoneTable(Base):
    __tablename__ = "milestones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    title = Column(String(255), nullable=False)
    target_date = Column(Date)
    completion_date = Column(Date)
    status = Column(String(50))
    progress_percentage = Column(Float)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    notes = Column(Text)

    task = relationship("TaskTable", foreign_keys=[task_id], back_populates="milestones")
    owner = relationship("UserTable", foreign_keys=[owner_id], back_populates="milestones")
