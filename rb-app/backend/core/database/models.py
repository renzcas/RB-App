from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    item_type = Column(String)  # "module" or "lab"
    item_id = Column(String)
    completed = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    action = Column(String)
    detail = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
