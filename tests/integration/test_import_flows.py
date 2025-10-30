"""
Integration tests for import flows
"""
import pytest
import json
from django.urls import reverse
from apps.imports.models import ImportJob
from apps.contacts.models import Contact
from unittest.mock import patch


@pytest.mark.django_db
@pytest.mark.integration
class TestImportFlows:
    """Test complete import flows"""
    
    def test_complete_csv_import_flow(self, authenticated_client, csv_file, user, mock_celery):
        """Test complete CSV import workflow"""
        # Step 1: Upload file
        with open(csv_file, 'rb') as f:
            response = authenticated_client.post(
                reverse('imports:upload'),
                {'file': f}
            )
            # Should show preview or redirect
            assert response.status_code in [200, 302]
        
        # Step 2: Create import job
        mapping = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email',
            'phone': 'phone',
            'company': 'company'
        }
        
        # Simulate starting import
        job = ImportJob.objects.create(
            user_id=str(user.id),
            filename='test.csv',
            status='PENDING',
            column_mapping=json.dumps(mapping)
        )
        
        # Step 3: Check progress
        response = authenticated_client.get(
            reverse('imports:progress', args=[job.id])
        )
        assert response.status_code == 200
        
        # Step 4: Check job status API
        response = authenticated_client.get(
            reverse('imports:job_status_api', args=[job.id])
        )
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data

