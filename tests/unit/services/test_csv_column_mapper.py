"""
Tests for CSV column mapper
"""
import pytest
import pandas as pd
from services.csv_column_mapper import CSVColumnMapper


class TestCSVColumnMapper:
    """Test CSVColumnMapper"""
    
    def test_mapper_initialization(self):
        """Test mapper can be initialized"""
        mapper = CSVColumnMapper()
        assert mapper.field_mappings is not None
        assert 'email' in mapper.field_mappings
    
    def test_auto_map_columns_exact_match(self):
        """Test auto map with exact column name match"""
        mapper = CSVColumnMapper()
        df = pd.DataFrame({
            'first_name': ['John'],
            'email': ['test@example.com'],
            'phone': ['+1234567890']
        })
        mapping = mapper.auto_map_columns(df)
        assert 'first_name' in mapping or 'email' in mapping
    
    def test_auto_map_columns_fuzzy_match(self):
        """Test auto map with fuzzy matching"""
        mapper = CSVColumnMapper()
        df = pd.DataFrame({
            'First Name': ['John'],
            'E-Mail': ['test@example.com'],
            'Phone Number': ['+1234567890']
        })
        mapping = mapper.auto_map_columns(df)
        # Should find matches based on keywords
        assert len(mapping) > 0
    
    def test_validate_mapping_no_duplicates(self):
        """Test validate mapping with no duplicates"""
        mapper = CSVColumnMapper()
        mapping = {
            'col1': 'first_name',
            'col2': 'last_name'
        }
        errors = mapper.validate_mapping(mapping)
        assert len(errors) == 0
    
    def test_validate_mapping_with_duplicates(self):
        """Test validate mapping with duplicate targets"""
        mapper = CSVColumnMapper()
        mapping = {
            'col1': 'email',
            'col2': 'email'  # Duplicate target
        }
        errors = mapper.validate_mapping(mapping)
        assert len(errors) > 0
    
    def test_apply_mapping(self):
        """Test apply mapping to DataFrame"""
        mapper = CSVColumnMapper()
        df = pd.DataFrame({
            'First Name': ['John'],
            'Last Name': ['Doe']
        })
        mapping = {
            'First Name': 'first_name',
            'Last Name': 'last_name'
        }
        mapped_df = mapper.apply_mapping(df, mapping)
        assert 'first_name' in mapped_df.columns or 'last_name' in mapped_df.columns

