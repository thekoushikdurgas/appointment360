"""
Import Error Tracker - Track errors during CSV import
"""
from typing import List, Dict
from datetime import datetime


class ImportError:
    def __init__(self, row_number: int, column: str, error_message: str, original_data: str):
        self.row_number = row_number
        self.column = column
        self.error_message = error_message
        self.original_data = original_data
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        return {
            'row_number': self.row_number,
            'column': self.column,
            'error_message': self.error_message,
            'original_data': self.original_data,
            'timestamp': self.timestamp.isoformat()
        }


class ImportErrorTracker:
    def __init__(self):
        self.errors: List[ImportError] = []
        self.error_summary: Dict[str, int] = {}
    
    def add_error(self, row_number: int, column: str, error_message: str, original_data: str):
        """Add an error to the tracker"""
        error = ImportError(row_number, column, error_message, original_data)
        self.errors.append(error)
        
        # Update error summary
        error_type = error_message.split(':')[0] if ':' in error_message else error_message
        self.error_summary[error_type] = self.error_summary.get(error_type, 0) + 1
    
    def get_errors(self) -> List[ImportError]:
        """Get all errors"""
        return self.errors
    
    def get_error_count(self) -> int:
        """Get total error count"""
        return len(self.errors)
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get error summary by type"""
        return self.error_summary
    
    def get_errors_by_type(self, error_type: str) -> List[ImportError]:
        """Get errors of specific type"""
        return [e for e in self.errors if error_type in e.error_message]
    
    def get_row_errors(self, row_number: int) -> List[ImportError]:
        """Get errors for specific row"""
        return [e for e in self.errors if e.row_number == row_number]
    
    def clear(self):
        """Clear all errors"""
        self.errors = []
        self.error_summary = {}
