import uuid

from sqlalchemy import JSON, UUID, Column, DateTime, Integer, String

from src.config.database.base_table import Base


class MarkdownFileTable(Base):
    __tablename__ = "markdown_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_path = Column(String(255))
    obsidian_vault = Column(String(255))
    last_modified = Column(DateTime)
    content_hash = Column(String(255))
    word_count = Column(Integer)
    linked_tasks = Column(JSON)
    backlinks_count = Column(Integer)
    frontmatter_data = Column(JSON)