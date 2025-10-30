"""
Validators - Input validation functions
"""
import re
from typing import Union


def validate_email(email: str) -> bool:
    """Validate email address"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate phone number"""
    if not phone:
        return False
    
    # Remove common separators
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it contains only digits and + sign
    pattern = r'^[\+]?[0-9]{7,15}$'
    return bool(re.match(pattern, phone))


def validate_url(url: str) -> bool:
    """Validate URL"""
    if not url:
        return False
    
    pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return bool(re.match(pattern, url))


def validate_numeric(value: Union[str, int, float]) -> bool:
    """Validate numeric value"""
    try:
        float(str(value))
        return True
    except ValueError:
        return False


def sanitize_string(value: str) -> str:
    """Sanitize string input"""
    if not value:
        return ""
    
    # Remove special characters but keep basic ones
    value = re.sub(r'[<>"\']', '', value)
    return value.strip()
