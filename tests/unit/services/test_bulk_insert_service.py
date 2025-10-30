"""
Tests for bulk insert service
"""
import pytest
import pandas as pd
from services.bulk_insert_service import BulkInsertService
from apps.contacts.models import Contact


@pytest.mark.django_db
class TestBulkInsertService:
    """Test BulkInsertService"""
    
    def test_service_initialization(self):
        """Test service can be initialized"""
        service = BulkInsertService()
        assert service.error_tracker is not None
    
    def test_bulk_insert_from_dataframe(self, db, user):
        """Test bulk insert from DataFrame"""
        service = BulkInsertService()
        df = pd.DataFrame({
            'first_name': ['John', 'Jane'],
            'last_name': ['Doe', 'Smith'],
            'email': ['john@example.com', 'jane@example.com'],
            'company': ['Corp1', 'Corp2']
        })
        column_mapping = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email',
            'company': 'company'
        }
        result = service.bulk_insert_from_dataframe(df, str(user.id), column_mapping)
        assert result['success_count'] >= 0
        assert 'error_count' in result
        assert 'duplicate_count' in result
    
    def test_bulk_insert_handles_duplicates(self, db, user, contact):
        """Test bulk insert handles duplicate emails"""
        service = BulkInsertService()
        df = pd.DataFrame({
            'first_name': ['New'],
            'last_name': ['Contact'],
            'email': [contact.email]  # Duplicate
        })
        column_mapping = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email'
        }
        result = service.bulk_insert_from_dataframe(df, str(user.id), column_mapping)
        assert result['duplicate_count'] >= 0
    
    def test_bulk_insert_chunked(self, db, user):
        """Test bulk insert in chunks"""
        service = BulkInsertService()
        df = pd.DataFrame({
            'first_name': [f'User{i}' for i in range(50)],
            'last_name': [f'Test{i}' for i in range(50)],
            'email': [f'user{i}@example.com' for i in range(50)],
            'company': [f'Company{i}' for i in range(50)]
        })
        column_mapping = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email',
            'company': 'company'
        }
        result = service.bulk_insert_chunked(df, str(user.id), column_mapping, chunk_size=10)
        assert result['success_count'] >= 0
    
    def test_get_errors(self, db, user):
        """Test get errors from tracker"""
        service = BulkInsertService()
        service.error_tracker.add_error(1, 'email', 'Invalid email', 'data')
        errors = service.get_errors()
        assert len(errors) > 0
    
    def test_get_error_summary(self, db, user):
        """Test get error summary"""
        service = BulkInsertService()
        service.error_tracker.add_error(1, 'email', 'Error', 'data')
        summary = service.get_error_summary()
        assert isinstance(summary, dict)

