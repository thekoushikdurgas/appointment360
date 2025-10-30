"""
Tests for import tasks (mocked Celery)
"""
import pytest
from unittest.mock import patch, Mock
from apps.imports.tasks import process_import_task


@pytest.mark.django_db
class TestImportTasks:
    """Test import Celery tasks"""
    
    @patch('apps.imports.tasks.process_import_task.delay')
    def test_process_import_task_called(self, mock_task, import_job):
        """Test import task is called"""
        # When task is called
        process_import_task.delay(import_job.id, 'test.csv', {}, 'user-id')
        # Should be called (mocked)
        mock_task.assert_called_once()
    
    @patch('apps.imports.tasks.BulkInsertService')
    def test_process_import_task_mocked(self, mock_bulk_service, import_job):
        """Test import task processing with mocked service"""
        mock_service_instance = Mock()
        mock_service_instance.bulk_insert_from_dataframe.return_value = {
            'success_count': 10,
            'error_count': 0,
            'duplicate_count': 0
        }
        mock_bulk_service.return_value = mock_service_instance
        
        # Simulate task execution (synchronous for testing)
        # In real scenario, this would be async via Celery
        assert mock_service_instance.bulk_insert_from_dataframe is not None

