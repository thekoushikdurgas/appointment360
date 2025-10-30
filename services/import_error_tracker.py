"""
Import Error Tracker - Track errors during CSV import
Migrated from Stremlit/services/import_error_tracker.py
"""
from typing import List, Dict, Any
from datetime import datetime
import json


class ImportError:
    """Represents a single import error"""
    
    def __init__(self, row_number: int, column: str, error_message: str, original_data: str):
        self.row_number = row_number
        self.column = column
        self.error_message = error_message
        self.original_data = original_data
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert error to dictionary"""
        return {
            'row_number': self.row_number,
            'column': self.column,
            'error_message': self.error_message,
            'original_data': self.original_data,
            'timestamp': self.timestamp.isoformat()
        }
    
    def to_json(self) -> str:
        """Convert error to JSON string"""
        return json.dumps(self.to_dict())
    
    def __str__(self):
        return f"Row {self.row_number}, Column '{self.column}': {self.error_message}"


class ImportErrorTracker:
    """Track and categorize errors during CSV import"""
    
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
    
    def add_duplicate_error(self, row_number: int, email: str):
        """Add a duplicate email error"""
        self.add_error(
            row_number,
            'email',
            'Duplicate email found',
            email
        )
    
    def add_validation_error(self, row_number: int, column: str, value: Any, reason: str):
        """Add a validation error"""
        self.add_error(
            row_number,
            column,
            f'Validation failed: {reason}',
            str(value)
        )
    
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
    
    def to_json(self) -> str:
        """Export errors as JSON"""
        errors_dict = [error.to_dict() for error in self.errors]
        return json.dumps({
            'errors': errors_dict,
            'summary': self.error_summary,
            'total_count': len(self.errors)
        }, default=str)
    
    def get_duplicate_count(self) -> int:
        """Get count of duplicate errors"""
        return len(self.get_errors_by_type('Duplicate'))
    
    def get_validation_error_count(self) -> int:
        """Get count of validation errors"""
        return len(self.get_errors_by_type('Validation'))

