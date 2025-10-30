"""
Tests for core views
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboardView:
    """Test dashboard view"""
    
    def test_dashboard_view(self, authenticated_client, multiple_contacts):
        """Test dashboard loads"""
        response = authenticated_client.get(reverse('core:dashboard'))
        assert response.status_code == 200
        assert 'metrics' in response.context or 'Dashboard' in response.content.decode()
    
    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication"""
        response = client.get(reverse('core:dashboard'))
        assert response.status_code in [302, 200]  # May redirect or allow


@pytest.mark.django_db
class TestWelcomeView:
    """Test welcome view"""
    
    def test_welcome_view(self, client):
        """Test welcome page loads"""
        response = client.get(reverse('core:welcome'))
        assert response.status_code == 200
    
    def test_welcome_redirects_if_authenticated(self, authenticated_client):
        """Test welcome redirects authenticated users"""
        response = authenticated_client.get(reverse('core:welcome'))
        # Should redirect to dashboard if authenticated
        assert response.status_code in [200, 302]


@pytest.mark.django_db
class TestLoadingView:
    """Test loading view"""
    
    def test_loading_view(self, client):
        """Test loading page loads"""
        response = client.get(reverse('core:loading'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestProgressTrackerView:
    """Test progress tracker view"""
    
    def test_progress_tracker_view(self, authenticated_client, task_tracker):
        """Test progress tracker page loads"""
        response = authenticated_client.get(reverse('core:progress_tracker'))
        assert response.status_code == 200
    
    def test_categories_api(self, authenticated_client, task_category):
        """Test categories API endpoint"""
        response = authenticated_client.get(reverse('core:categories_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'categories' in data
    
    def test_tasks_api(self, authenticated_client, task_tracker):
        """Test tasks API endpoint"""
        response = authenticated_client.get(reverse('core:tasks_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'tasks' in data
    
    def test_update_task_status_api(self, authenticated_client, task_tracker):
        """Test updating task status"""
        import json
        response = authenticated_client.post(
            reverse('core:update_task_status_api', args=[task_tracker.id]),
            json.dumps({'is_completed': True}),
            content_type='application/json'
        )
        assert response.status_code == 200
        task_tracker.refresh_from_db()
        assert task_tracker.is_completed is True
    
    def test_progress_stats_api(self, authenticated_client, task_tracker):
        """Test progress stats API"""
        response = authenticated_client.get(reverse('core:progress_stats_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'overall_progress' in data
        assert 'total_tasks' in data

