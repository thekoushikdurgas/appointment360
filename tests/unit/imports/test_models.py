"""
Tests for imports models
"""
import pytest
from django.utils import timezone
from apps.imports.models import ImportJob


@pytest.mark.django_db
class TestImportJob:
    """Test ImportJob model"""
    
    def test_import_job_creation(self, import_job):
        """Test import job can be created"""
        assert import_job.status == 'PENDING'
        assert import_job.total_rows == 100
        assert import_job.processed_rows == 0
    
    def test_import_job_progress_percentage(self, import_job):
        """Test progress percentage calculation"""
        assert import_job.get_progress_percentage() == 0.0
        import_job.processed_rows = 50
        import_job.save()
        assert import_job.get_progress_percentage() == 50.0
    
    def test_import_job_is_complete(self, import_job):
        """Test is_complete method"""
        assert import_job.is_complete() is False
        import_job.status = 'COMPLETED'
        import_job.save()
        assert import_job.is_complete() is True
    
    def test_import_job_is_running(self, import_job):
        """Test is_running method"""
        assert import_job.is_running() is False
        import_job.status = 'PROCESSING'
        import_job.save()
        assert import_job.is_running() is True
    
    def test_import_job_str_method(self, import_job):
        """Test import job string representation"""
        assert str(import_job).startswith('ImportJob')
        assert import_job.filename in str(import_job)

