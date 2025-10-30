"""
File Path Validation Service
Validates local file paths for CSV imports
Migrated from Stremlit/services/file_validator.py
"""
import os
from pathlib import Path
from typing import Tuple
from django.conf import settings


class FileValidator:
    """Validate file paths for CSV imports"""
    
    ALLOWED_EXTENSIONS = ['.csv', '.CSV']
    MAX_FILE_SIZE_MB = 100  # 100MB max file size
    
    @staticmethod
    def validate_local_path(file_path: str) -> Tuple[bool, str]:
        """
        Validate local file path exists and is CSV
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file path is empty
        if not file_path or not file_path.strip():
            return False, "File path cannot be empty"
        
        # Convert to Path object for easier handling
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return False, f"File not found: {file_path}"
        
        # Check if it's a file (not a directory)
        if not path.is_file():
            return False, f"Path is not a file: {file_path}"
        
        # Check file extension
        if path.suffix.lower() not in FileValidator.ALLOWED_EXTENSIONS:
            return False, f"Invalid file extension. Allowed: {', '.join(FileValidator.ALLOWED_EXTENSIONS)}"
        
        # Check if file is readable
        if not os.access(path, os.R_OK):
            return False, f"File is not readable: {file_path}"
        
        # Check file size
        try:
            file_size = path.stat().st_size
            if file_size == 0:
                return False, "File is empty"
            
            # Check if file size exceeds max limit
            file_size_mb = file_size / (1024 * 1024)
            if file_size_mb > FileValidator.MAX_FILE_SIZE_MB:
                return False, f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size ({FileValidator.MAX_FILE_SIZE_MB} MB)"
        except OSError as e:
            return False, f"Cannot access file: {e}"
        
        return True, "File is valid"
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """Get file size in MB"""
        try:
            path = Path(file_path)
            if path.exists():
                size_bytes = path.stat().st_size
                return size_bytes / (1024 * 1024)
            return 0.0
        except Exception:
            return 0.0
    
    @staticmethod
    def list_csv_files(directory: str) -> list:
        """List all CSV files in a directory"""
        csv_files = []
        try:
            path = Path(directory)
            if path.exists() and path.is_dir():
                for file in path.glob('*.csv'):
                    csv_files.append(str(file.absolute()))
                for file in path.glob('*.CSV'):
                    csv_files.append(str(file.absolute()))
        except Exception as e:
            print(f"Error listing CSV files: {e}")
        
        return sorted(csv_files)
    
    @staticmethod
    def should_use_pyspark(file_path: str, threshold_mb: float = 10.0) -> bool:
        """
        Determine if PySpark should be used for processing
        
        Args:
            file_path: Path to the file
            threshold_mb: Size threshold in MB (default: 10MB)
            
        Returns:
            True if file size exceeds threshold
        """
        file_size_mb = FileValidator.get_file_size_mb(file_path)
        return file_size_mb > threshold_mb

