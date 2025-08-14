import uuid

from sqlalchemy import JSON, UUID, Column, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class UserPatternTable(Base):
    __tablename__ = "user_patterns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    productive_hours = Column(JSON)
    task_preferences = Column(JSON)
    velocity_data = Column(JSON)
    break_patterns = Column(JSON)
    burnout_risk_score = Column(Float)
    preferred_task_duration = Column(Float)

    user = relationship("UserTable", foreign_keys=[user_id], back_populates="patterns")
