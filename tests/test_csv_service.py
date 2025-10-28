"""
Tests for CSV Service
"""
import pytest
import pandas as pd
import io
from services.csv_service import CSVService
from services.csv_column_mapper import CSVColumnMapper


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing"""
    return """first_name,last_name,email,phone,company,industry
John,Doe,john.doe@example.com,+1234567890,Acme Corp,Technology
Jane,Smith,jane.smith@example.com,+1234567891,Tech Inc,Technology
Bob,Johnson,bob.johnson@example.com,+1234567892,Health Co,Healthcare
"""


def test_read_csv():
    """Test reading CSV"""
    service = CSVService()
    
    csv_data = """name,email,phone
John Doe,john@example.com,+1234567890
"""
    
    df = service.read_csv(io.StringIO(csv_data))
    
    assert df is not None
    assert len(df) == 1
    assert 'email' in df.columns


def test_validate_csv():
    """Test CSV validation"""
    service = CSVService()
    
    # Valid CSV
    df_valid = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith'],
        'email': ['john@example.com', 'jane@example.com']
    })
    
    is_valid, errors = service.validate_csv(df_valid, required_columns=['name', 'email'])
    
    assert is_valid
    assert len(errors) == 0
    
    # Invalid CSV - missing required column
    df_invalid = pd.DataFrame({
        'name': ['John Doe'],
        'other': ['value']
    })
    
    is_valid, errors = service.validate_csv(df_invalid, required_columns=['name', 'email'])
    
    assert not is_valid
    assert len(errors) > 0


def test_process_chunks():
    """Test chunked processing"""
    service = CSVService()
    
    # Create large dataframe
    data = {
        'name': [f'Person {i}' for i in range(5000)],
        'email': [f'person{i}@example.com' for i in range(5000)]
    }
    df = pd.DataFrame(data)
    
    chunks = service.process_chunks(df, chunk_size=1000)
    
    assert len(chunks) == 5  # 5000 / 1000


def test_auto_detect_columns():
    """Test auto-detection of columns"""
    service = CSVService()
    
    # Create dataframe with various column names
    df = pd.DataFrame({
        'first name': ['John'],
        'E-Mail': ['john@example.com'],
        'Phone Number': ['+1234567890'],
        'Company Name': ['Acme Corp'],
        'City': ['New York']
    })
    
    mapping = service.auto_detect_columns(df)
    
    assert 'first name' in mapping
    assert mapping['first name'] == 'first_name'
    assert 'E-Mail' in mapping
    assert mapping['E-Mail'] == 'email'


def test_export_to_csv():
    """Test exporting to CSV"""
    service = CSVService()
    
    df = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith'],
        'email': ['john@example.com', 'jane@example.com']
    })
    
    csv_bytes = service.export_to_csv(df)
    
    assert csv_bytes is not None
    assert len(csv_bytes) > 0
    assert b'name,email' in csv_bytes


def test_export_to_excel():
    """Test exporting to Excel"""
    service = CSVService()
    
    df = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith'],
        'email': ['john@example.com', 'jane@example.com']
    })
    
    excel_bytes = service.export_to_excel(df)
    
    assert excel_bytes is not None
    assert len(excel_bytes) > 0


def test_column_mapper_auto_map():
    """Test automatic column mapping"""
    mapper = CSVColumnMapper()
    
    df = pd.DataFrame({
        'First Name': ['John'],
        'Email Address': ['john@example.com'],
        'Phone': ['+1234567890'],
        'Company': ['Acme Corp']
    })
    
    mapping = mapper.auto_map_columns(df)
    
    assert 'First Name' in mapping
    assert 'Email Address' in mapping
    assert 'Phone' in mapping
    assert 'Company' in mapping


def test_column_mapper_validate():
    """Test mapping validation"""
    mapper = CSVColumnMapper()
    
    # Valid mapping
    valid_mapping = {
        'csv_col1': 'field1',
        'csv_col2': 'field2'
    }
    
    errors = mapper.validate_mapping(valid_mapping)
    assert len(errors) == 0
    
    # Duplicate mapping
    invalid_mapping = {
        'csv_col1': 'field1',
        'csv_col2': 'field1'
    }
    
    errors = mapper.validate_mapping(invalid_mapping)
    assert len(errors) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

