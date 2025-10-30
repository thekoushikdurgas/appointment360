"""
Settings models for user preferences and feature toggles
"""
from django.db import models
from django.conf import settings


class UserSettings(models.Model):
    """User-specific settings and preferences"""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    
    # UI Preferences
    theme = models.CharField(
        max_length=20,
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('auto', 'Auto'),
        ],
        default='light'
    )
    
    language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
        ],
        default='en'
    )
    
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Dashboard Preferences
    dashboard_layout = models.CharField(
        max_length=20,
        choices=[
            ('grid', 'Grid'),
            ('list', 'List'),
            ('compact', 'Compact'),
        ],
        default='grid'
    )
    
    items_per_page = models.IntegerField(default=20)
    
    # Notification Preferences
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    import_completion_notifications = models.BooleanField(default=True)
    export_completion_notifications = models.BooleanField(default=True)
    error_notifications = models.BooleanField(default=True)
    
    # Feature Toggles
    enable_analytics = models.BooleanField(default=True)
    enable_bulk_operations = models.BooleanField(default=True)
    enable_progress_tracking = models.BooleanField(default=True)
    enable_export_history = models.BooleanField(default=True)
    enable_data_quality_reports = models.BooleanField(default=True)
    
    # Import/Export Settings
    default_import_format = models.CharField(
        max_length=10,
        choices=[
            ('csv', 'CSV'),
            ('excel', 'Excel'),
            ('json', 'JSON'),
        ],
        default='csv'
    )
    
    default_export_format = models.CharField(
        max_length=10,
        choices=[
            ('csv', 'CSV'),
            ('excel', 'Excel'),
            ('json', 'JSON'),
        ],
        default='csv'
    )
    
    auto_delete_temp_files = models.BooleanField(default=True)
    temp_file_retention_days = models.IntegerField(default=7)
    
    # Security Settings
    two_factor_enabled = models.BooleanField(default=False)
    session_timeout_minutes = models.IntegerField(default=480)  # 8 hours
    
    # Privacy Settings
    data_retention_days = models.IntegerField(default=365)
    allow_data_sharing = models.BooleanField(default=False)
    allow_analytics_tracking = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Settings"
        verbose_name_plural = "User Settings"
    
    def __str__(self):
        return f"Settings for {self.user.username}"


class FeatureToggle(models.Model):
    """Global feature toggles for the application"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=True)
    is_global = models.BooleanField(default=True)  # If False, users can override
    
    # Feature categories
    category = models.CharField(
        max_length=50,
        choices=[
            ('ui', 'User Interface'),
            ('import', 'Import Features'),
            ('export', 'Export Features'),
            ('analytics', 'Analytics'),
            ('security', 'Security'),
            ('performance', 'Performance'),
            ('integration', 'Integration'),
        ],
        default='ui'
    )
    
    # Rollout settings
    rollout_percentage = models.IntegerField(default=100)  # Percentage of users to enable for
    target_user_groups = models.JSONField(default=list, blank=True)  # Specific user groups
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Feature Toggle"
        verbose_name_plural = "Feature Toggles"
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({'Enabled' if self.is_enabled else 'Disabled'})"
    
    def is_enabled_for_user(self, user):
        """Check if feature is enabled for a specific user"""
        if not self.is_enabled:
            return False
        
        if self.is_global:
            return True
        
        # Check user-specific override
        try:
            user_toggle = UserFeatureToggle.objects.get(
                user=user,
                feature=self
            )
            return user_toggle.is_enabled
        except UserFeatureToggle.DoesNotExist:
            return self.is_enabled


class UserFeatureToggle(models.Model):
    """User-specific feature toggle overrides"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feature = models.ForeignKey(FeatureToggle, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'feature']
        verbose_name = "User Feature Toggle"
        verbose_name_plural = "User Feature Toggles"
    
    def __str__(self):
        return f"{self.user.username} - {self.feature.name} ({'Enabled' if self.is_enabled else 'Disabled'})"


class SystemSettings(models.Model):
    """System-wide settings and configuration"""
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    
    # Setting categories
    category = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General'),
            ('import', 'Import Settings'),
            ('export', 'Export Settings'),
            ('analytics', 'Analytics'),
            ('security', 'Security'),
            ('performance', 'Performance'),
            ('email', 'Email Settings'),
            ('storage', 'Storage Settings'),
        ],
        default='general'
    )
    
    # Data type for validation
    data_type = models.CharField(
        max_length=20,
        choices=[
            ('string', 'String'),
            ('integer', 'Integer'),
            ('boolean', 'Boolean'),
            ('json', 'JSON'),
            ('float', 'Float'),
        ],
        default='string'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"
        ordering = ['category', 'key']
    
    def __str__(self):
        return f"{self.key} = {self.value}"
    
    def get_typed_value(self):
        """Get the value converted to its proper type"""
        if self.data_type == 'integer':
            try:
                return int(self.value)
            except ValueError:
                return 0
        elif self.data_type == 'boolean':
            return self.value.lower() in ['true', '1', 'yes', 'on']
        elif self.data_type == 'float':
            try:
                return float(self.value)
            except ValueError:
                return 0.0
        elif self.data_type == 'json':
            try:
                import json
                return json.loads(self.value)
            except (ValueError, TypeError):
                return {}
        else:
            return self.value
    
    def set_typed_value(self, value):
        """Set the value with proper type conversion"""
        if self.data_type == 'json':
            import json
            self.value = json.dumps(value)
        else:
            self.value = str(value)
