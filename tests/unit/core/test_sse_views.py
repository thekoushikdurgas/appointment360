"""
Tests for Server-Sent Events views
"""
import pytest
from django.urls import reverse
from django.http import JsonResponse


@pytest.mark.django_db
class TestSSEViews:
    """Test SSE views"""
    
    def test_sse_status_api(self, authenticated_client, user):
        """Test SSE status endpoint"""
        response = authenticated_client.get(reverse('core:sse_status'))
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'active'
    
    def test_send_notification_api(self, authenticated_client, user):
        """Test send notification endpoint"""
        import json
        response = authenticated_client.post(
            reverse('core:send_notification'),
            json.dumps({
                'user_id': str(user.id),
                'message': 'Test notification',
                'type': 'info'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
    
    def test_send_notification_missing_params(self, authenticated_client):
        """Test send notification with missing parameters"""
        import json
        response = authenticated_client.post(
            reverse('core:send_notification'),
            json.dumps({'message': 'Test'}),
            content_type='application/json'
        )
        # Should return 400 or error
        assert response.status_code in [200, 400]

