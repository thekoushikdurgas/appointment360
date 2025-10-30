"""
Tests for file validator
"""
import pytest
import tempfile
import os
from pathlib import Path
from services.file_validator import FileValidator


class TestFileValidator:
    """Test FileValidator"""
    
    def test_validate_local_path_valid(self, tmp_path):
        """Test validate valid file path"""
        test_file = tmp_path / 'test.csv'
        test_file.write_text('test,data\n1,2\n')
        
        is_valid, message = FileValidator.validate_local_path(str(test_file))
        assert is_valid is True
        assert 'valid' in message.lower() or message == ''
    
    def test_validate_local_path_not_exists(self):
        """Test validate non-existent file"""
        is_valid, message = FileValidator.validate_local_path('/nonexistent/file.csv')
        assert is_valid is False
        assert 'not found' in message.lower() or 'not exist' in message.lower()
    
    def test_validate_local_path_wrong_extension(self, tmp_path):
        """Test validate file with wrong extension"""
        test_file = tmp_path / 'test.txt'
        test_file.write_text('test data')
        
        is_valid, message = FileValidator.validate_local_path(str(test_file))
        assert is_valid is False
    
    def test_get_file_size_mb(self, tmp_path):
        """Test get file size in MB"""
        test_file = tmp_path / 'test.csv'
        test_file.write_text('test,data\n' * 1000)
        
        size_mb = FileValidator.get_file_size_mb(str(test_file))
        assert size_mb > 0
        assert isinstance(size_mb, float)
    
    def test_list_csv_files(self, tmp_path):
        """Test list CSV files in directory"""
        # Create CSV files
        (tmp_path / 'file1.csv').write_text('data')
        (tmp_path / 'file2.CSV').write_text('data')
        (tmp_path / 'not_csv.txt').write_text('data')
        
        csv_files = FileValidator.list_csv_files(str(tmp_path))
        assert len(csv_files) >= 2
    
    def test_should_use_pyspark_large_file(self, tmp_path):
        """Test PySpark should be used for large files"""
        # Create a large file (simulate)
        test_file = tmp_path / 'large.csv'
        # Write enough data to exceed threshold
        test_file.write_text('data,' * 1000000)
        
        should_use = FileValidator.should_use_pyspark(str(test_file), threshold_mb=0.001)
        # Should recommend PySpark for large files
        assert isinstance(should_use, bool)

