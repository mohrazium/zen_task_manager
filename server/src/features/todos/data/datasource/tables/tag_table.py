import enum
import uuid
from datetime import datetime

from sqlalchemy import (JSON, UUID, Boolean, Column, Date, DateTime, Enum,
                        Float, ForeignKey, Integer, String, Table, Text, Time)
from sqlalchemy.orm import declarative_base, relationship

from src.config.database.base_table import Base


class TagTable(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entity_tags.id"), nullable=False)
    color = Column(String(50), nullable=False)
    icon = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    name = Column(String(100), unique=True, nullable=False)

    entities = relationship("EntityTagTable", foreign_keys=[entity_id], back_populates="tag")


class EntityTagTable(Base):
    __tablename__ = "entity_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    entity_type = Column(String(50), nullable=False)  # e.g., 'task', 'project'
    entity_id = Column(UUID(as_uuid=True), nullable=False)

    tag = relationship("TagTable", foreign_keys=[tag_id], back_populates="entities")
