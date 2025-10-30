"""
Helper functions
"""
from typing import Any, Dict
from datetime import datetime


def format_date(date: datetime) -> str:
    """Format datetime to string"""
    if date is None:
        return ""
    return date.strftime("%Y-%m-%d %H:%M:%S")


def format_date_short(date: datetime) -> str:
    """Format datetime to short string"""
    if date is None:
        return ""
    return date.strftime("%Y-%m-%d")


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from dictionary"""
    return {k: v for k, v in data.items() if v is not None}


def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return filename.split('.')[-1].lower() if '.' in filename else ""


def format_number(num: int) -> str:
    """Format number with thousand separator"""
    return f"{num:,}"
