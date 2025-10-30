"""
Type Converter - Convert CSV values to appropriate database types
"""
import pandas as pd
from typing import Any, Optional
from decimal import Decimal
import re


class TypeConverter:
    """Convert CSV data types to database-compatible types"""
    
    # Fields that should be integers
    INTEGER_FIELDS = {
        'employees_count',
        'annual_revenue',
        'total_funding',
        'latest_funding_amount',
        'user_id'
    }
    
    # Fields that should be booleans
    BOOLEAN_FIELDS = {
        'is_active'
    }
    
    # Fields that should be floats
    FLOAT_FIELDS = {
        'revenue',
        'total_funding',
        'latest_funding_amount'
    }
    
    @staticmethod
    def is_integer(value: Any) -> bool:
        """Check if value can be converted to integer"""
        if value is None or pd.isna(value):
            return False
        
        # Try to convert string to int
        try:
            # Handle float strings like "9427000.0"
            if isinstance(value, (int, float)):
                return float(value).is_integer()
            elif isinstance(value, str):
                # Try to parse as float first, then check if it's an integer
                float_val = float(value)
                return float_val.is_integer()
            return False
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def to_integer(value: Any) -> Optional[int]:
        """Convert value to integer"""
        if value is None or pd.isna(value):
            return None
        
        try:
            if isinstance(value, (int, float)):
                return int(value)
            elif isinstance(value, str):
                # Parse string to float first, then convert to int
                value_clean = value.strip()
                if not value_clean:
                    return None
                float_val = float(value_clean)
                if float_val.is_integer():
                    return int(float_val)
                else:
                    # Round if it's a decimal
                    return int(round(float_val))
            return None
        except (ValueError, TypeError, AttributeError):
            return None
    
    @staticmethod
    def is_boolean(value: Any) -> bool:
        """Check if value can be converted to boolean"""
        if value is None or pd.isna(value):
            return False
        
        if isinstance(value, bool):
            return True
        elif isinstance(value, str):
            return value.lower() in ['true', '1', 'yes', 'active', 't']
        elif isinstance(value, (int, float)):
            return value in [0, 1]
        return False
    
    @staticmethod
    def to_boolean(value: Any) -> bool:
        """Convert value to boolean"""
        if value is None or pd.isna(value):
            return True  # Default to True
        
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ['true', '1', 'yes', 'active', 't']
        elif isinstance(value, (int, float)):
            return bool(value)
        return True
    
    @staticmethod
    def convert_value(field_name: str, value: Any) -> Any:
        """Convert value based on field name and type"""
        # Handle None/NaN
        if value is None or pd.isna(value):
            # Return None for integer fields, empty string for others
            if field_name in TypeConverter.INTEGER_FIELDS:
                return None
            return None if pd.isna(value) else value
        
        # Convert to string and strip whitespace first
        value_str = str(value).strip() if value else ""
        
        # Check if it's empty
        if not value_str or value_str.lower() in ['nan', 'none', 'null', '']:
            return None if field_name in TypeConverter.INTEGER_FIELDS else ""
        
        # Convert based on field type
        if field_name in TypeConverter.INTEGER_FIELDS:
            return TypeConverter.to_integer(value)
        elif field_name in TypeConverter.BOOLEAN_FIELDS:
            return TypeConverter.to_boolean(value)
        else:
            # For string fields, just return the cleaned value
            return value_str
    
    @staticmethod
    def clean_contact_data(contact_data: dict) -> dict:
        """Clean and convert contact data to proper types"""
        cleaned_data = {}
        
        for field, value in contact_data.items():
            cleaned_data[field] = TypeConverter.convert_value(field, value)
        
        return cleaned_data

