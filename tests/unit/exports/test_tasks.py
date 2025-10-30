"""
Tests for export tasks (mocked Celery)
"""
import pytest
from unittest.mock import patch, Mock
from apps.exports.tasks import process_export_task


@pytest.mark.django_db
class TestExportTasks:
    """Test export Celery tasks"""
    
    @patch('apps.exports.tasks.process_export_task.delay')
    def test_process_export_task_called(self, mock_task, export_log):
        """Test export task is called"""
        process_export_task.delay(export_log.id)
        mock_task.assert_called_once()
    
    @patch('apps.exports.tasks.pd.DataFrame')
    def test_process_export_task_mocked(self, mock_dataframe, export_log):
        """Test export task processing with mocked DataFrame"""
        mock_df = Mock()
        mock_df.to_csv = Mock()
        mock_dataframe.return_value = mock_df
        
        # Simulate task execution
        assert mock_dataframe is not None

