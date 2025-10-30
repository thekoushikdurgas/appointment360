"""
Integration tests for analytics flows
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.integration
class TestAnalyticsFlows:
    """Test complete analytics flows"""
    
    def test_complete_analytics_flow(self, authenticated_client, multiple_contacts):
        """Test complete analytics dashboard flow"""
        # Step 1: Access analytics dashboard
        response = authenticated_client.get(reverse('analytics:dashboard'))
        assert response.status_code == 200
        
        # Step 2: Access data quality page
        response = authenticated_client.get(reverse('analytics:data_quality'))
        assert response.status_code == 200
        
        # Step 3: Get chart data
        response = authenticated_client.get(
            reverse('analytics:chart_data_api', args=['industry'])
        )
        assert response.status_code == 200
        
        # Step 4: Get analytics stats
        response = authenticated_client.get(reverse('analytics:analytics_stats_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'total_contacts' in data

