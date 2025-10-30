"""
Tests for jobs views
"""
import pytest
from django.urls import reverse
from unittest.mock import patch, Mock


@pytest.mark.django_db
class TestJobScraperView:
    """Test job scraper view"""
    
    def test_job_scraper_view_get(self, authenticated_client):
        """Test job scraper page loads"""
        response = authenticated_client.get(reverse('jobs:scraper'))
        assert response.status_code == 200
    
    @patch('apps.jobs.views.run_scraper_async')
    def test_job_scraper_view_post(self, mock_run_scraper, authenticated_client):
        """Test job scraper with URL"""
        mock_run_scraper.return_value = [
            {'title': 'Job 1', 'company': 'Company 1'},
            {'title': 'Job 2', 'company': 'Company 2'}
        ]
        
        response = authenticated_client.post(
            reverse('jobs:scraper'),
            {'url': 'https://example.com/jobs'}
        )
        assert response.status_code in [200, 302]
    
    def test_job_scraper_view_no_url(self, authenticated_client):
        """Test job scraper without URL"""
        response = authenticated_client.post(
            reverse('jobs:scraper'),
            {}
        )
        assert response.status_code == 200
    
    def test_job_results_view(self, authenticated_client):
        """Test job results page"""
        # Set session data
        session = authenticated_client.session
        session['scraped_jobs'] = [{'title': 'Test Job'}]
        session['scraped_url'] = 'https://example.com'
        session.save()
        
        response = authenticated_client.get(reverse('jobs:results'))
        assert response.status_code == 200
    
    def test_job_scraper_api(self, authenticated_client):
        """Test job scraper API endpoint"""
        import json
        with patch('apps.jobs.views.run_scraper_async') as mock_scraper:
            mock_scraper.return_value = [{'title': 'Test Job'}]
            response = authenticated_client.post(
                reverse('jobs:api_scrape'),
                json.dumps({'url': 'https://example.com'}),
                content_type='application/json'
            )
            assert response.status_code == 200
    
    def test_job_scraper_status_api(self, authenticated_client):
        """Test job scraper status API"""
        response = authenticated_client.get(reverse('jobs:api_status'))
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data

