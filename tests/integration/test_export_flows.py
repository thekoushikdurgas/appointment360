"""
Integration tests for export flows
"""
import pytest
import json
from django.urls import reverse
from apps.exports.models import ExportLog
from apps.contacts.models import Contact


@pytest.mark.django_db
@pytest.mark.integration
class TestExportFlows:
    """Test complete export flows"""
    
    def test_complete_export_flow(self, authenticated_client, multiple_contacts, export_limit, mock_celery):
        """Test complete export workflow"""
        # Step 1: Create export via API
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
        
        # Step 2: Check export history
        response = authenticated_client.get(reverse('exports:history'))
        assert response.status_code == 200
        
        # Step 3: Get export status (if export was created)
        exports = ExportLog.objects.all()
        if exports.exists():
            export = exports.first()
            response = authenticated_client.get(
                reverse('exports:export_status_api', args=[export.id])
            )
            assert response.status_code == 200

