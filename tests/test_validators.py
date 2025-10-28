"""
Tests for Validators
"""
import pytest
from utils.validators import (
    validate_email,
    validate_phone,
    validate_url,
    validate_numeric,
    sanitize_string
)


def test_validate_email():
    """Test email validation"""
    assert validate_email("test@example.com") == True
    assert validate_email("user.name@example.co.uk") == True
    assert validate_email("test@test") == False
    assert validate_email("notanemail") == False
    assert validate_email("") == False


def test_validate_phone():
    """Test phone validation"""
    assert validate_phone("+1234567890") == True
    assert validate_phone("1234567890") == True
    assert validate_phone("+1 234 567 890") == True
    assert validate_phone("123") == False
    assert validate_phone("") == False


def test_validate_url():
    """Test URL validation"""
    assert validate_url("https://example.com") == True
    assert validate_url("http://example.com/path") == True
    assert validate_url("not a url") == False
    assert validate_url("") == False


def test_validate_numeric():
    """Test numeric validation"""
    assert validate_numeric("123") == True
    assert validate_numeric(123) == True
    assert validate_numeric("12.34") == True
    assert validate_numeric("not numeric") == False


def test_sanitize_string():
    """Test string sanitization"""
    assert sanitize_string("normal text") == "normal text"
    assert sanitize_string("<script>alert('xss')</script>") == "scriptalertxssscript"
    assert sanitize_string("test with 'quotes'") == "test with quotes"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

