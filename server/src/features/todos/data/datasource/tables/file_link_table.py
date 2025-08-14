import uuid

from sqlalchemy import UUID, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from src.config.database.base_table import Base


class FileLinkTable(Base):
    __tablename__ = "file_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_file_id = Column(UUID(as_uuid=True), ForeignKey("markdown_files.id"))
    target_file_id = Column(UUID(as_uuid=True), ForeignKey("markdown_files.id"))
    link_type = Column(String(50))
    context_snippet = Column(Text)

    source_file = relationship("MarkdownFileTable", foreign_keys=[source_file_id], back_populates="source_links")
    target_file = relationship("MarkdownFileTable", foreign_keys=[target_file_id], back_populates="target_files")

