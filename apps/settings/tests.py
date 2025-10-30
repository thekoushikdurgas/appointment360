"""
Tests for the Settings functionality
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.settings.models import UserSettings, FeatureToggle, UserFeatureToggle, SystemSettings
import json


class SettingsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create test feature toggles
        self.feature1 = FeatureToggle.objects.create(
            name='Test Feature 1',
            description='A test feature',
            category='ui',
            is_enabled=True,
            is_global=False
        )
        
        self.feature2 = FeatureToggle.objects.create(
            name='Test Feature 2',
            description='Another test feature',
            category='ui',
            is_enabled=True,
            is_global=True
        )
        
        # Create test system settings
        self.system_setting = SystemSettings.objects.create(
            key='test_setting',
            value='test_value',
            description='A test system setting',
            category='general',
            data_type='string'
        )

    def test_settings_page_view(self):
        """Test the settings page loads correctly"""
        response = self.client.get(reverse('settings:settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Settings')
        self.assertContains(response, 'General Settings')

    def test_user_settings_creation(self):
        """Test that user settings are created automatically"""
        # Settings should be created when accessing the page
        response = self.client.get(reverse('settings:settings'))
        self.assertEqual(response.status_code, 200)
        
        # Check that UserSettings was created
        user_settings = UserSettings.objects.get(user=self.user)
        self.assertIsNotNone(user_settings)
        self.assertEqual(user_settings.theme, 'light')
        self.assertEqual(user_settings.language, 'en')

    def test_update_user_settings_api(self):
        """Test updating user settings via API"""
        # Create user settings first
        user_settings = UserSettings.objects.create(user=self.user)
        
        # Update settings
        update_data = {
            'theme': 'dark',
            'language': 'es',
            'items_per_page': 50,
            'email_notifications': False
        }
        
        response = self.client.post(
            reverse('settings:update_user_settings'),
            json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Verify settings were updated
        user_settings.refresh_from_db()
        self.assertEqual(user_settings.theme, 'dark')
        self.assertEqual(user_settings.language, 'es')
        self.assertEqual(user_settings.items_per_page, 50)
        self.assertFalse(user_settings.email_notifications)

    def test_toggle_feature_api(self):
        """Test toggling feature via API"""
        # Test toggling non-global feature
        response = self.client.post(
            reverse('settings:toggle_feature', args=[self.feature1.id])
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['is_enabled'])
        
        # Verify user feature toggle was created
        user_toggle = UserFeatureToggle.objects.get(
            user=self.user,
            feature=self.feature1
        )
        self.assertFalse(user_toggle.is_enabled)
        
        # Test toggling global feature (should fail)
        response = self.client.post(
            reverse('settings:toggle_feature', args=[self.feature2.id])
        )
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('globally controlled', data['error'])

    def test_get_user_settings_api(self):
        """Test getting user settings via API"""
        # Create user settings
        user_settings = UserSettings.objects.create(
            user=self.user,
            theme='dark',
            language='fr'
        )
        
        response = self.client.get(reverse('settings:get_user_settings_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('settings', data)
        self.assertIn('feature_toggles', data)
        
        # Check settings data
        settings = data['settings']
        self.assertEqual(settings['theme'], 'dark')
        self.assertEqual(settings['language'], 'fr')
        
        # Check feature toggles data
        features = data['feature_toggles']
        self.assertEqual(len(features), 2)
        self.assertEqual(features[0]['name'], 'Test Feature 1')

    def test_feature_toggle_for_user(self):
        """Test feature toggle logic for users"""
        # Test global feature (should be enabled)
        self.assertTrue(self.feature2.is_enabled_for_user(self.user))
        
        # Test non-global feature (should be enabled by default)
        self.assertTrue(self.feature1.is_enabled_for_user(self.user))
        
        # Create user override
        UserFeatureToggle.objects.create(
            user=self.user,
            feature=self.feature1,
            is_enabled=False
        )
        
        # Test with user override
        self.assertFalse(self.feature1.is_enabled_for_user(self.user))

    def test_reset_settings(self):
        """Test resetting settings to defaults"""
        # Create user settings with custom values
        user_settings = UserSettings.objects.create(
            user=self.user,
            theme='dark',
            language='es',
            items_per_page=50
        )
        
        # Create user feature override
        UserFeatureToggle.objects.create(
            user=self.user,
            feature=self.feature1,
            is_enabled=False
        )
        
        # Reset settings
        response = self.client.post(reverse('settings:reset_settings'))
        self.assertEqual(response.status_code, 302)  # Redirect after reset
        
        # Verify settings were reset
        with self.assertRaises(UserSettings.DoesNotExist):
            UserSettings.objects.get(user=self.user)
        
        with self.assertRaises(UserFeatureToggle.DoesNotExist):
            UserFeatureToggle.objects.get(user=self.user, feature=self.feature1)

    def test_export_settings(self):
        """Test exporting settings"""
        # Create user settings
        user_settings = UserSettings.objects.create(
            user=self.user,
            theme='dark',
            language='es'
        )
        
        response = self.client.get(reverse('settings:export_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertIn('user_settings', data)
        self.assertIn('feature_overrides', data)
        self.assertIn('exported_at', data)
        self.assertEqual(data['user'], 'testuser')

    def test_system_settings_model(self):
        """Test SystemSettings model methods"""
        # Test get_typed_value
        self.assertEqual(self.system_setting.get_typed_value(), 'test_value')
        
        # Test set_typed_value
        self.system_setting.set_typed_value('new_value')
        self.assertEqual(self.system_setting.value, 'new_value')
        
        # Test JSON data type
        json_setting = SystemSettings.objects.create(
            key='json_setting',
            value='{"key": "value"}',
            data_type='json'
        )
        self.assertEqual(json_setting.get_typed_value(), {'key': 'value'})
        
        json_setting.set_typed_value({'new': 'data'})
        self.assertEqual(json_setting.value, '{"new": "data"}')

    def test_unauthorized_access(self):
        """Test that unauthorized users cannot access settings"""
        self.client.logout()
        
        response = self.client.get(reverse('settings:settings'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        response = self.client.get(reverse('settings:get_user_settings_api'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_invalid_feature_toggle(self):
        """Test toggling non-existent feature"""
        response = self.client.post(
            reverse('settings:toggle_feature', args=[99999])
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_settings_update(self):
        """Test updating settings with invalid data"""
        response = self.client.post(
            reverse('settings:update_user_settings'),
            'invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
