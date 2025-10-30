"""
Settings views for user preferences and feature toggles
"""
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import UserSettings, FeatureToggle, UserFeatureToggle, SystemSettings


@login_required
def settings_page(request):
    """Main settings page"""
    # Get or create user settings
    user_settings, created = UserSettings.objects.get_or_create(
        user=request.user,
        defaults={
            'theme': 'light',
            'language': 'en',
            'timezone': 'UTC',
            'dashboard_layout': 'grid',
            'items_per_page': 20,
            'email_notifications': True,
            'push_notifications': True,
            'import_completion_notifications': True,
            'export_completion_notifications': True,
            'error_notifications': True,
            'enable_analytics': True,
            'enable_bulk_operations': True,
            'enable_progress_tracking': True,
            'enable_export_history': True,
            'enable_data_quality_reports': True,
            'default_import_format': 'csv',
            'default_export_format': 'csv',
            'auto_delete_temp_files': True,
            'temp_file_retention_days': 7,
            'two_factor_enabled': False,
            'session_timeout_minutes': 480,
            'data_retention_days': 365,
            'allow_data_sharing': False,
            'allow_analytics_tracking': True,
        }
    )
    
    # Get feature toggles
    feature_toggles = FeatureToggle.objects.filter(is_enabled=True).order_by('category', 'name')
    
    # Get user-specific feature overrides
    user_feature_overrides = {
        override.feature.id: override.is_enabled
        for override in UserFeatureToggle.objects.filter(user=request.user)
    }
    
    # Get system settings
    system_settings = SystemSettings.objects.all().order_by('category', 'key')
    
    context = {
        'page_title': 'Settings',
        'user_settings': user_settings,
        'feature_toggles': feature_toggles,
        'user_feature_overrides': user_feature_overrides,
        'system_settings': system_settings,
        'theme_choices': UserSettings._meta.get_field('theme').choices,
        'language_choices': UserSettings._meta.get_field('language').choices,
        'dashboard_layout_choices': UserSettings._meta.get_field('dashboard_layout').choices,
        'format_choices': UserSettings._meta.get_field('default_import_format').choices,
        'category_choices': FeatureToggle._meta.get_field('category').choices,
    }
    
    return render(request, 'settings/settings.html', context)


@login_required
@require_http_methods(["POST"])
def update_user_settings(request):
    """Update user settings via AJAX"""
    try:
        data = json.loads(request.body)
        
        # Get or create user settings
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        
        # Update settings based on the data received
        for field, value in data.items():
            if hasattr(user_settings, field):
                setattr(user_settings, field, value)
        
        user_settings.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Settings updated successfully'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def toggle_feature(request, feature_id):
    """Toggle a feature for the current user"""
    try:
        feature = FeatureToggle.objects.get(id=feature_id)
        
        # Check if user can override this feature
        if feature.is_global:
            return JsonResponse({
                'success': False,
                'error': 'This feature is globally controlled and cannot be overridden'
            }, status=400)
        
        # Get or create user feature toggle
        user_toggle, created = UserFeatureToggle.objects.get_or_create(
            user=request.user,
            feature=feature,
            defaults={'is_enabled': True}
        )
        
        # Toggle the setting
        user_toggle.is_enabled = not user_toggle.is_enabled
        user_toggle.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Feature {feature.name} {"enabled" if user_toggle.is_enabled else "disabled"}',
            'is_enabled': user_toggle.is_enabled
        })
    
    except FeatureToggle.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Feature not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def get_user_settings_api(request):
    """API endpoint to get user settings"""
    try:
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        
        # Get feature toggles with user overrides
        feature_toggles = []
        for feature in FeatureToggle.objects.filter(is_enabled=True):
            is_enabled = feature.is_enabled_for_user(request.user)
            feature_toggles.append({
                'id': feature.id,
                'name': feature.name,
                'description': feature.description,
                'category': feature.category,
                'is_enabled': is_enabled,
                'is_global': feature.is_global
            })
        
        return JsonResponse({
            'success': True,
            'settings': {
                'theme': user_settings.theme,
                'language': user_settings.language,
                'timezone': user_settings.timezone,
                'dashboard_layout': user_settings.dashboard_layout,
                'items_per_page': user_settings.items_per_page,
                'email_notifications': user_settings.email_notifications,
                'push_notifications': user_settings.push_notifications,
                'import_completion_notifications': user_settings.import_completion_notifications,
                'export_completion_notifications': user_settings.export_completion_notifications,
                'error_notifications': user_settings.error_notifications,
                'enable_analytics': user_settings.enable_analytics,
                'enable_bulk_operations': user_settings.enable_bulk_operations,
                'enable_progress_tracking': user_settings.enable_progress_tracking,
                'enable_export_history': user_settings.enable_export_history,
                'enable_data_quality_reports': user_settings.enable_data_quality_reports,
                'default_import_format': user_settings.default_import_format,
                'default_export_format': user_settings.default_export_format,
                'auto_delete_temp_files': user_settings.auto_delete_temp_files,
                'temp_file_retention_days': user_settings.temp_file_retention_days,
                'two_factor_enabled': user_settings.two_factor_enabled,
                'session_timeout_minutes': user_settings.session_timeout_minutes,
                'data_retention_days': user_settings.data_retention_days,
                'allow_data_sharing': user_settings.allow_data_sharing,
                'allow_analytics_tracking': user_settings.allow_analytics_tracking,
            },
            'feature_toggles': feature_toggles
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def reset_settings(request):
    """Reset user settings to defaults"""
    try:
        # Delete existing settings
        UserSettings.objects.filter(user=request.user).delete()
        
        # Delete user feature overrides
        UserFeatureToggle.objects.filter(user=request.user).delete()
        
        messages.success(request, 'Settings reset to defaults successfully')
        return redirect('settings:settings')
    
    except Exception as e:
        messages.error(request, f'Error resetting settings: {str(e)}')
        return redirect('settings:settings')


@login_required
def export_settings(request):
    """Export user settings as JSON"""
    try:
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        
        # Get user feature overrides
        user_feature_overrides = UserFeatureToggle.objects.filter(user=request.user)
        
        settings_data = {
            'user_settings': {
                'theme': user_settings.theme,
                'language': user_settings.language,
                'timezone': user_settings.timezone,
                'dashboard_layout': user_settings.dashboard_layout,
                'items_per_page': user_settings.items_per_page,
                'email_notifications': user_settings.email_notifications,
                'push_notifications': user_settings.push_notifications,
                'import_completion_notifications': user_settings.import_completion_notifications,
                'export_completion_notifications': user_settings.export_completion_notifications,
                'error_notifications': user_settings.error_notifications,
                'enable_analytics': user_settings.enable_analytics,
                'enable_bulk_operations': user_settings.enable_bulk_operations,
                'enable_progress_tracking': user_settings.enable_progress_tracking,
                'enable_export_history': user_settings.enable_export_history,
                'enable_data_quality_reports': user_settings.enable_data_quality_reports,
                'default_import_format': user_settings.default_import_format,
                'default_export_format': user_settings.default_export_format,
                'auto_delete_temp_files': user_settings.auto_delete_temp_files,
                'temp_file_retention_days': user_settings.temp_file_retention_days,
                'two_factor_enabled': user_settings.two_factor_enabled,
                'session_timeout_minutes': user_settings.session_timeout_minutes,
                'data_retention_days': user_settings.data_retention_days,
                'allow_data_sharing': user_settings.allow_data_sharing,
                'allow_analytics_tracking': user_settings.allow_analytics_tracking,
            },
            'feature_overrides': [
                {
                    'feature_name': override.feature.name,
                    'is_enabled': override.is_enabled
                }
                for override in user_feature_overrides
            ],
            'exported_at': timezone.now().isoformat(),
            'user': request.user.username
        }
        
        response = JsonResponse(settings_data, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename="settings_{request.user.username}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
        
        return response
    
    except Exception as e:
        messages.error(request, f'Error exporting settings: {str(e)}')
        return redirect('settings:settings')


@login_required
@require_http_methods(["POST"])
def import_settings(request):
    """Import user settings from JSON file"""
    try:
        if 'settings_file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No file uploaded'
            }, status=400)
        
        settings_file = request.FILES['settings_file']
        
        # Read and parse JSON
        settings_data = json.loads(settings_file.read().decode('utf-8'))
        
        # Validate data structure
        if 'user_settings' not in settings_data:
            return JsonResponse({
                'success': False,
                'error': 'Invalid settings file format'
            }, status=400)
        
        # Get or create user settings
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        
        # Update settings
        for field, value in settings_data['user_settings'].items():
            if hasattr(user_settings, field):
                setattr(user_settings, field, value)
        
        user_settings.save()
        
        # Update feature overrides if present
        if 'feature_overrides' in settings_data:
            # Clear existing overrides
            UserFeatureToggle.objects.filter(user=request.user).delete()
            
            # Create new overrides
            for override_data in settings_data['feature_overrides']:
                try:
                    feature = FeatureToggle.objects.get(name=override_data['feature_name'])
                    UserFeatureToggle.objects.create(
                        user=request.user,
                        feature=feature,
                        is_enabled=override_data['is_enabled']
                    )
                except FeatureToggle.DoesNotExist:
                    continue
        
        return JsonResponse({
            'success': True,
            'message': 'Settings imported successfully'
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON file'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
