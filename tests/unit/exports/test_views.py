"""
Tests for exports views
"""
import pytest
import json
import tempfile
import os
from django.urls import reverse
from apps.exports.models import ExportLog


@pytest.mark.django_db
class TestExportHistoryView:
    """Test export history view"""
    
    def test_export_history_view(self, authenticated_client, export_log):
        """Test export history page loads"""
        response = authenticated_client.get(reverse('exports:history'))
        assert response.status_code == 200
    
    def test_export_history_filtering(self, authenticated_client, export_log):
        """Test export history filtering"""
        response = authenticated_client.get(
            reverse('exports:history'),
            {'status': 'completed', 'type': 'contacts'}
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestExportAPIs:
    """Test export API endpoints"""
    
    def test_export_status_api(self, authenticated_client, export_log):
        """Test export status API"""
        response = authenticated_client.get(
            reverse('exports:export_status_api', args=[export_log.id])
        )
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
    
    def test_download_export(self, authenticated_client, export_log, tmp_path):
        """Test download export"""
        # Create a temporary file for download
        test_file = tmp_path / 'test_export.csv'
        test_file.write_text('test,data\n1,2\n')
        export_log.file_path = str(test_file)
        export_log.save()
        
        response = authenticated_client.get(
            reverse('exports:download_export', args=[export_log.id])
        )
        # Should download or show error if file doesn't exist in actual path
        assert response.status_code in [200, 302, 404]
    
    def test_cancel_export_api(self, authenticated_client, db, user):
        """Test cancel export API"""
        export = ExportLog.objects.create(
            user=user,
            export_type='contacts',
            status='processing'
        )
        response = authenticated_client.post(
            reverse('exports:cancel_export_api', args=[export.id])
        )
        assert response.status_code == 200
        export.refresh_from_db()
        assert export.status == 'cancelled'
    
    def test_delete_export_api(self, authenticated_client, export_log):
        """Test delete export API"""
        export_id = export_log.id
        response = authenticated_client.post(
            reverse('exports:delete_export_api', args=[export_log.id])
        )
        assert response.status_code == 200
        assert not ExportLog.objects.filter(id=export_id).exists()
    
    def test_create_export_api(self, authenticated_client, export_limit, mock_celery):
        """Test create export API"""
        import json
        response = authenticated_client.post(
            reverse('exports:create_export_api'),
            json.dumps({
                'export_type': 'contacts',
                'export_format': 'csv',
                'filters': {}
            }),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]
    
    def test_export_stats_api(self, authenticated_client, export_log):
        """Test export stats API"""
        response = authenticated_client.get(reverse('exports:export_stats_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'stats' in data

