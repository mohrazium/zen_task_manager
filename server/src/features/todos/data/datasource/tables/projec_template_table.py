import uuid

from sqlalchemy import JSON, UUID, Column, Float, String

from server.src.config.database.base_table import Base


class ProjectTemplateTable(Base):
    __tablename__ = "project_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phases = Column(JSON)
    estimated_duration = Column(Float)  # in weeks
    category = Column(String(50))
    complexity_level = Column(String(50))
    target_audience = Column(String(255))
    recommended_tools = Column(JSON)
