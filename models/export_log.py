"""
Export Log Model
"""
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from datetime import datetime
from config.database import Base
import enum


class ExportType(PyEnum):
    """Types of exports"""
    CONTACTS = "contacts"
    ANALYTICS = "analytics"
    HISTORY = "history"


class ExportFormat(PyEnum):
    """Export file formats"""
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"
    JSON = "json"


class ExportLog(Base):
    """Track all exports for limits and auditing"""
    __tablename__ = "export_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)  # UUID string from Supabase
    export_type = Column(String, nullable=False)
    export_format = Column(String, nullable=False)
    record_count = Column(Integer, default=0)
    filename = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ExportLog {self.export_type} ({self.export_format}) - {self.record_count} records>"

