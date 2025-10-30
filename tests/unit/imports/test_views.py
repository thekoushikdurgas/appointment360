"""
Tests for imports views
"""
import pytest
import json
from django.urls import reverse
from apps.imports.models import ImportJob


@pytest.mark.django_db
class TestUploadView:
    """Test upload view"""
    
    def test_upload_view_get(self, authenticated_client):
        """Test upload page loads"""
        response = authenticated_client.get(reverse('imports:upload'))
        assert response.status_code == 200
    
    def test_upload_view_with_file(self, authenticated_client, csv_file_object):
        """Test file upload"""
        with open(csv_file_object.name, 'rb') if hasattr(csv_file_object, 'name') else csv_file_object as f:
            response = authenticated_client.post(
                reverse('imports:upload'),
                {'file': csv_file_object}
            )
            # Should redirect to preview or show preview
            assert response.status_code in [200, 302]


@pytest.mark.django_db
class TestStartImportView:
    """Test start import view"""
    
    def test_start_import_view(self, authenticated_client, import_job, csv_file, mock_celery):
        """Test starting import"""
        mapping = {'first_name': 'first_name', 'email': 'email'}
        response = authenticated_client.post(
            reverse('imports:start'),
            {
                'file_path': csv_file,
                'mapping': json.dumps(mapping)
            }
        )
        assert response.status_code in [200, 302]


@pytest.mark.django_db
class TestProgressView:
    """Test progress view"""
    
    def test_progress_view(self, authenticated_client, import_job):
        """Test progress page loads"""
        response = authenticated_client.get(
            reverse('imports:progress', args=[import_job.id])
        )
        assert response.status_code == 200
    
    def test_job_status_api(self, authenticated_client, import_job):
        """Test job status API"""
        response = authenticated_client.get(
            reverse('imports:job_status_api', args=[import_job.id])
        )
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert 'progress_percentage' in data
    
    def test_cancel_job_api(self, authenticated_client, import_job):
        """Test cancel job API"""
        import_job.status = 'PROCESSING'
        import_job.save()
        
        response = authenticated_client.post(
            reverse('imports:cancel_job_api', args=[import_job.id])
        )
        assert response.status_code == 200
        import_job.refresh_from_db()
        assert import_job.status == 'CANCELLED'
    
    def test_recent_jobs_api(self, authenticated_client, import_job):
        """Test recent jobs API"""
        response = authenticated_client.get(reverse('imports:recent_jobs_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'jobs' in data

