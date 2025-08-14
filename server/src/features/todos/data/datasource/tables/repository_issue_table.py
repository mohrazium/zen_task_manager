import uuid

from click import DateTime
from sqlalchemy import (JSON, UUID, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class RepositoryIssueTable(Base):
    __tablename__ = "repository_issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    issue_id = Column(Integer, nullable=False)
    repository = Column(String(255))
    status = Column(String(50))
    title = Column(String(255))
    labels = Column(JSON)
    assignee = Column(String(100))
    closed_at = Column(DateTime)

    task = relationship("TaskTable", foreign_keys=[task_id], back_populates="repository_issues")
