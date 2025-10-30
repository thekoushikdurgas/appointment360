"""
Export Limit Service - Handle download limits and tracking
"""
from typing import Dict, Tuple
from config.settings import DEFAULT_DOWNLOAD_LIMIT
from models.export_log import ExportLog, ExportFormat, ExportType
from config.database import SessionLocal


class ExportLimitService:
    def __init__(self, db_session):
        self.db = db_session
        self.default_limit = DEFAULT_DOWNLOAD_LIMIT
    
    def get_user_limit(self, user_id: int) -> int:
        """Get user's download limit"""
        # In a real implementation, this would fetch from user model
        # For now, return default limit
        return self.default_limit
    
    def check_limit(self, user_id: int) -> Tuple[bool, int]:
        """Check if user can export"""
        # Get user limit
        limit = self.get_user_limit(user_id)
        
        # Count user's exports today
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        count = self.db.query(ExportLog).filter(
            ExportLog.user_id == user_id,
            ExportLog.created_at >= today
        ).count()
        
        remaining = limit - count
        can_export = remaining > 0
        
        return can_export, remaining
    
    def log_export(self, user_id: int, export_type: ExportType, 
                   export_format: ExportFormat, record_count: int, 
                   filename: str = None):
        """Log export event"""
        export_log = ExportLog(
            user_id=user_id,
            export_type=export_type,
            export_format=export_format,
            record_count=record_count,
            filename=filename
        )
        self.db.add(export_log)
        self.db.commit()
    
    def get_export_statistics(self, user_id: int) -> Dict:
        """Get export statistics for user"""
        total = self.db.query(ExportLog).filter(
            ExportLog.user_id == user_id
        ).count()
        
        # Today's count
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        today_count = self.db.query(ExportLog).filter(
            ExportLog.user_id == user_id,
            ExportLog.created_at >= today
        ).count()
        
        return {
            'total_exports': total,
            'today_exports': today_count,
            'remaining': max(0, self.get_user_limit(user_id) - today_count)
        }
