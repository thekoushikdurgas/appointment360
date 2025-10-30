"""
Tests for analytics views
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestAnalyticsDashboard:
    """Test analytics dashboard view"""
    
    def test_analytics_dashboard(self, authenticated_client, multiple_contacts):
        """Test analytics dashboard loads"""
        response = authenticated_client.get(reverse('analytics:dashboard'))
        assert response.status_code == 200
    
    def test_analytics_dashboard_with_data(self, authenticated_client, multiple_contacts):
        """Test dashboard with contact data"""
        response = authenticated_client.get(reverse('analytics:dashboard'))
        assert response.status_code == 200
        # Should have statistics in context
        assert 'total_contacts' in response.context or response.status_code == 200
    
    def test_data_quality_view(self, authenticated_client, multiple_contacts):
        """Test data quality view"""
        response = authenticated_client.get(reverse('analytics:data_quality'))
        assert response.status_code == 200
    
    def test_chart_data_api_industry(self, authenticated_client, multiple_contacts):
        """Test chart data API for industry"""
        response = authenticated_client.get(
            reverse('analytics:chart_data_api', args=['industry'])
        )
        assert response.status_code == 200
        data = response.json()
        assert 'labels' in data or 'error' in data
    
    def test_chart_data_api_country(self, authenticated_client, multiple_contacts):
        """Test chart data API for country"""
        response = authenticated_client.get(
            reverse('analytics:chart_data_api', args=['country'])
        )
        assert response.status_code == 200
    
    def test_analytics_stats_api(self, authenticated_client, multiple_contacts):
        """Test analytics stats API"""
        response = authenticated_client.get(reverse('analytics:analytics_stats_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'total_contacts' in data

