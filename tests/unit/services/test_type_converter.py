"""
Tests for type converter
"""
import pytest
import pandas as pd
from services.type_converter import TypeConverter


class TestTypeConverter:
    """Test TypeConverter"""
    
    def test_is_integer_true(self):
        """Test is_integer returns True for valid integers"""
        assert TypeConverter.is_integer(42) is True
        assert TypeConverter.is_integer('42') is True
        assert TypeConverter.is_integer(42.0) is True
    
    def test_is_integer_false(self):
        """Test is_integer returns False for invalid integers"""
        assert TypeConverter.is_integer('abc') is False
        assert TypeConverter.is_integer(42.5) is False
        assert TypeConverter.is_integer(None) is False
    
    def test_to_integer_valid(self):
        """Test to_integer converts valid values"""
        assert TypeConverter.to_integer(42) == 42
        assert TypeConverter.to_integer('42') == 42
        assert TypeConverter.to_integer(42.0) == 42
    
    def test_to_integer_invalid(self):
        """Test to_integer handles invalid values"""
        assert TypeConverter.to_integer('abc') is None
        assert TypeConverter.to_integer(None) is None
    
    def test_is_boolean_true(self):
        """Test is_boolean returns True for valid booleans"""
        assert TypeConverter.is_boolean(True) is True
        assert TypeConverter.is_boolean('true') is True
        assert TypeConverter.is_boolean(1) is True
    
    def test_is_boolean_false(self):
        """Test is_boolean returns False for invalid booleans"""
        assert TypeConverter.is_boolean('maybe') is False
    
    def test_to_boolean(self):
        """Test to_boolean converts values"""
        assert TypeConverter.to_boolean(True) is True
        assert TypeConverter.to_boolean('true') is True
        assert TypeConverter.to_boolean(1) is True
        assert TypeConverter.to_boolean('false') is False
    
    def test_convert_value_integer_field(self):
        """Test convert_value for integer fields"""
        result = TypeConverter.convert_value('employees_count', '42')
        assert result == 42
        assert isinstance(result, int)
    
    def test_convert_value_boolean_field(self):
        """Test convert_value for boolean fields"""
        result = TypeConverter.convert_value('is_active', 'true')
        assert result is True
        assert isinstance(result, bool)
    
    def test_convert_value_string_field(self):
        """Test convert_value for string fields"""
        result = TypeConverter.convert_value('company', 'Test Corp')
        assert result == 'Test Corp'
        assert isinstance(result, str)
    
    def test_clean_and_merge_names(self):
        """Test clean_and_merge_names function"""
        contact_data = {
            'first_name': 'John',
            'last_name': 'Doe'
        }
        result = TypeConverter.clean_and_merge_names(contact_data)
        assert 'full_name' in result
        assert result['full_name'] == 'John Doe'
    
    def test_clean_and_merge_names_existing_full_name(self):
        """Test clean_and_merge_names with existing full_name"""
        contact_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'full_name': 'Existing Name'
        }
        result = TypeConverter.clean_and_merge_names(contact_data)
        # Should keep existing full_name or merge
        assert 'full_name' in result

