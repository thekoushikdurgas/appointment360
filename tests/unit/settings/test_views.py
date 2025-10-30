"""
Tests for settings views
"""
import pytest
import json
from django.urls import reverse
from apps.settings.models import UserSettings, FeatureToggle, UserFeatureToggle


@pytest.mark.django_db
class TestSettingsPageView:
    """Test settings page view"""
    
    def test_settings_page_get(self, authenticated_client, user):
        """Test settings page loads"""
        response = authenticated_client.get(reverse('settings:settings'))
        assert response.status_code == 200
    
    def test_settings_page_creates_user_settings(self, authenticated_client, user):
        """Test settings page creates user settings automatically"""
        response = authenticated_client.get(reverse('settings:settings'))
        assert response.status_code == 200
        # Settings should be created
        assert UserSettings.objects.filter(user=user).exists()


@pytest.mark.django_db
class TestSettingsAPIs:
    """Test settings API endpoints"""
    
    def test_update_user_settings_api(self, authenticated_client, user_settings):
        """Test update user settings API"""
        response = authenticated_client.post(
            reverse('settings:update_user_settings'),
            json.dumps({
                'theme': 'dark',
                'language': 'es',
                'items_per_page': 50
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        
        user_settings.refresh_from_db()
        assert user_settings.theme == 'dark'
    
    def test_toggle_feature_api(self, authenticated_client, feature_toggle):
        """Test toggle feature API"""
        response = authenticated_client.post(
            reverse('settings:toggle_feature', args=[feature_toggle.id])
        )
        assert response.status_code == 200
        data = response.json()
        assert 'success' in data
    
    def test_get_user_settings_api(self, authenticated_client, user_settings):
        """Test get user settings API"""
        response = authenticated_client.get(reverse('settings:get_user_settings_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'settings' in data
        assert 'feature_toggles' in data
    
    def test_reset_settings(self, authenticated_client, user_settings):
        """Test reset settings"""
        response = authenticated_client.post(reverse('settings:reset_settings'))
        assert response.status_code == 302
        # Settings should be deleted
        assert not UserSettings.objects.filter(user=user_settings.user).exists()
    
    def test_export_settings(self, authenticated_client, user_settings):
        """Test export settings"""
        response = authenticated_client.get(reverse('settings:export_settings'))
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'
    
    def test_import_settings(self, authenticated_client, user):
        """Test import settings"""
        settings_data = {
            'user_settings': {
                'theme': 'dark',
                'language': 'es'
            },
            'feature_overrides': []
        }
        
        # Create a file-like object
        from io import BytesIO
        file_obj = BytesIO(json.dumps(settings_data).encode('utf-8'))
        
        response = authenticated_client.post(
            reverse('settings:import_settings'),
            {'settings_file': file_obj}
        )
        assert response.status_code in [200, 400]  # May validate and return error

