from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseTable(Base):
    __tablename__ = 'base_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    info = Column(String)