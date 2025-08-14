

import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class ProjectIssueTable(Base):
    __tablename__ = "project_issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    repository_issue_id = Column(UUID(as_uuid=True), ForeignKey("repository_issues.id"))
    status = Column(String(50))
    priority = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime)

    project = relationship("ProjectTable", foreign_keys=[project_id], back_populates="issues")
    repository_issue = relationship("RepositoryIssueTable", foreign_keys=[repository_issue_id], back_populates="project_issues")
