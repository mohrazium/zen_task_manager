import uuid

from sqlalchemy import (JSON, UUID, Column, Float, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class PhaseTable(Base):
    __tablename__ = "phases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("project_templates.id"))
    title = Column(String(255))
    duration_weeks = Column(Float)
    order_index = Column(Integer)
    milestone_ids = Column(JSON)
    description = Column(Text)

    template = relationship("ProjectTemplateTable", foreign_keys=[template_id], back_populates="phases")
