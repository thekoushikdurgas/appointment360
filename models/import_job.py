"""
Import Job Model - Track background import jobs
"""
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base


class ImportJob(Base):
    """Import job model for tracking background import jobs"""
    __tablename__ = "import_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Job Information
    user_id = Column(String, nullable=True)  # UUID string from Supabase
    filename = Column(String, nullable=False)
    file_size = Column(BigInteger)  # File size in bytes (supports large files up to 9.2 exabytes)
    
    # Progress Tracking
    total_rows = Column(Integer, default=0)
    processed_rows = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    duplicate_count = Column(Integer, default=0)
    
    # Status
    status = Column(
        String,
        default="PENDING",
        index=True
    )  # PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED
    
    # Timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Metadata
    error_log = Column(Text)  # JSON string of errors
    column_mapping = Column(Text)  # JSON string of column mappings
    
    # Performance Metrics
    processing_speed = Column(Float)  # rows per second
    estimated_completion = Column(DateTime, nullable=True)
    
    # Batch Information
    current_batch = Column(Integer, default=0)
    total_batches = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ImportJob {self.id}: {self.filename} ({self.status})>"
    
    def get_progress_percentage(self) -> float:
        """Calculate progress percentage"""
        if self.total_rows == 0:
            return 0.0
        return (self.processed_rows / self.total_rows) * 100
    
    def is_complete(self) -> bool:
        """Check if job is complete"""
        return self.status in ['COMPLETED', 'FAILED', 'CANCELLED']
    
    def is_running(self) -> bool:
        """Check if job is currently running"""
        return self.status == 'PROCESSING'
    
    def get_remaining_rows(self) -> int:
        """Get number of rows remaining"""
        return max(0, self.total_rows - self.processed_rows)

