"""
Tests for Bulk Insert Service
"""
import pytest
from sqlalchemy.orm import Session
from services.bulk_insert_service import BulkInsertService
from config.database import get_db


@pytest.fixture
def db_session():
    """Create database session"""
    db = next(get_db())
    yield db
    db.close()


@pytest.fixture
def bulk_service(db_session):
    """Create bulk insert service"""
    return BulkInsertService(db_session)


def test_row_to_dict(bulk_service):
    """Test conversion of row to dictionary"""
    # Mock row
    class MockRow:
        def get(self, key, default=None):
            data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone': '123-456-7890',
                'company': 'Test Corp',
                'industry': 'Tech',
                'employees_count': 100,
                'annual_revenue': 1000000,
            }
            return data.get(key, default)
    
    row = MockRow()
    result = bulk_service._row_to_dict(row, user_id=1)
    
    assert result is not None
    assert result['first_name'] == 'John'
    assert result['email'] == 'john@example.com'
    assert result['user_id'] == 1


def test_build_full_name(bulk_service):
    """Test building full name from first and last name"""
    # Mock row with both names
    class MockRow:
        def get(self, key, default=None):
            data = {
                'first_name': 'John',
                'last_name': 'Doe',
            }
            return data.get(key, default)
    
    row = MockRow()
    full_name = bulk_service._build_full_name(row)
    
    assert full_name == 'John Doe'


def test_build_full_name_missing_last(bulk_service):
    """Test building full name when last name is missing"""
    # Mock row without last name
    class MockRow:
        def get(self, key, default=None):
            data = {
                'first_name': 'John',
                'last_name': '',
            }
            return data.get(key, default)
    
    row = MockRow()
    full_name = bulk_service._build_full_name(row)
    
    assert full_name == 'John'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

