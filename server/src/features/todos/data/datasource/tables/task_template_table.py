import uuid

from sqlalchemy import JSON, UUID, Column, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class TaskTemplateTable(Base):
    __tablename__ = "task_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phase_id = Column(UUID(as_uuid=True), ForeignKey("phases.id"))
    title = Column(String(255))
    description = Column(Text)
    estimated_hours = Column(Float)
    prerequisites = Column(JSON)
    default_priority = Column(String(50))
    recommended_tools = Column(JSON)
    ai_difficulty_score = Column(Float)

    phase = relationship("PhaseTable", foreign_keys=[phase_id], back_populates="task_templates")