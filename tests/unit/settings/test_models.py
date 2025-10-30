"""
Tests for settings models
"""
import pytest
from apps.settings.models import UserSettings, FeatureToggle, UserFeatureToggle, SystemSettings


@pytest.mark.django_db
class TestUserSettings:
    """Test UserSettings model"""
    
    def test_user_settings_creation(self, user_settings):
        """Test user settings can be created"""
        assert user_settings.theme == 'light'
        assert user_settings.language == 'en'
        assert user_settings.items_per_page == 20
    
    def test_user_settings_str_method(self, user_settings):
        """Test user settings string representation"""
        assert user_settings.user.username in str(user_settings)


@pytest.mark.django_db
class TestFeatureToggle:
    """Test FeatureToggle model"""
    
    def test_feature_toggle_creation(self, feature_toggle):
        """Test feature toggle can be created"""
        assert feature_toggle.name == 'Test Feature'
        assert feature_toggle.is_enabled is True
        assert feature_toggle.is_global is False
    
    def test_feature_toggle_is_enabled_for_user(self, feature_toggle, user):
        """Test is_enabled_for_user method"""
        # Without user override, should return toggle's enabled state
        assert feature_toggle.is_enabled_for_user(user) is True
        
        # With user override disabled
        UserFeatureToggle.objects.create(
            user=user,
            feature=feature_toggle,
            is_enabled=False
        )
        assert feature_toggle.is_enabled_for_user(user) is False


@pytest.mark.django_db
class TestSystemSettings:
    """Test SystemSettings model"""
    
    def test_system_setting_creation(self, system_setting):
        """Test system setting can be created"""
        assert system_setting.key == 'test_setting'
        assert system_setting.value == 'test_value'
    
    def test_system_setting_get_typed_value_string(self, system_setting):
        """Test get typed value for string"""
        assert system_setting.get_typed_value() == 'test_value'
    
    def test_system_setting_get_typed_value_integer(self, db):
        """Test get typed value for integer"""
        setting = SystemSettings.objects.create(
            key='int_setting',
            value='42',
            data_type='integer'
        )
        assert setting.get_typed_value() == 42
    
    def test_system_setting_get_typed_value_boolean(self, db):
        """Test get typed value for boolean"""
        setting = SystemSettings.objects.create(
            key='bool_setting',
            value='true',
            data_type='boolean'
        )
        assert setting.get_typed_value() is True
    
    def test_system_setting_set_typed_value(self, db):
        """Test set typed value"""
        setting = SystemSettings.objects.create(
            key='test_setting',
            value='old_value',
            data_type='string'
        )
        setting.set_typed_value('new_value')
        assert setting.value == 'new_value'

