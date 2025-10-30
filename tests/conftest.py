"""
Pytest configuration and shared fixtures
"""
import pytest
import tempfile
import os
from pathlib import Path
from io import BytesIO
from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from unittest.mock import Mock, patch, MagicMock
from apps.contacts.models import Contact
from apps.imports.models import ImportJob
from apps.exports.models import ExportLog, ExportLimit
from apps.core.models import TaskTracker, TaskCategory
from apps.settings.models import UserSettings, FeatureToggle, UserFeatureToggle, SystemSettings

User = get_user_model()


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker):
    """Setup database for tests"""
    pass


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        is_active=True
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user"""
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        is_staff=True,
        is_superuser=True,
        is_active=True
    )


@pytest.fixture
def authenticated_client(client, user):
    """Create an authenticated test client"""
    client.force_login(user)
    return client


@pytest.fixture
def contact(db, user):
    """Create a test contact"""
    return Contact.objects.create(
        first_name='John',
        last_name='Doe',
        full_name='John Doe',
        email='john.doe@example.com',
        phone='+1234567890',
        company='Example Corp',
        industry='Technology',
        city='San Francisco',
        state='CA',
        country='USA',
        is_active=True
    )


@pytest.fixture
def multiple_contacts(db, user):
    """Create multiple test contacts"""
    contacts = []
    for i in range(10):
        contact = Contact.objects.create(
            first_name=f'User{i}',
            last_name=f'Test{i}',
            full_name=f'User{i} Test{i}',
            email=f'user{i}@example.com',
            company=f'Company{i}',
            industry=['Technology', 'Finance', 'Healthcare'][i % 3],
            country=['USA', 'Canada', 'UK'][i % 3],
            is_active=True
        )
        contacts.append(contact)
    return contacts


@pytest.fixture
def import_job(db, user):
    """Create a test import job"""
    return ImportJob.objects.create(
        user_id=str(user.id),
        filename='test_contacts.csv',
        file_size=1024,
        total_rows=100,
        processed_rows=0,
        status='PENDING',
        column_mapping='{}'
    )


@pytest.fixture
def export_log(db, user):
    """Create a test export log"""
    return ExportLog.objects.create(
        user=user,
        export_type='contacts',
        export_format='csv',
        status='completed',
        record_count=50,
        file_size=5000,
        filename='contacts_export.csv'
    )


@pytest.fixture
def export_limit(db, user):
    """Create a test export limit"""
    return ExportLimit.objects.get_or_create(
        user_id=str(user.id),
        defaults={'limit': 100, 'export_count': 0}
    )[0]


@pytest.fixture
def task_category(db):
    """Create a test task category"""
    return TaskCategory.objects.create(
        name='Test Category',
        description='Test Description',
        color='#007bff',
        icon='fas fa-test',
        order=1,
        is_active=True
    )


@pytest.fixture
def task_tracker(db, task_category):
    """Create a test task tracker"""
    return TaskTracker.objects.create(
        category='SETUP',
        task_name='Test Task',
        description='Test Description',
        priority='HIGH',
        order=1,
        is_completed=False
    )


@pytest.fixture
def user_settings(db, user):
    """Create test user settings"""
    return UserSettings.objects.create(
        user=user,
        theme='light',
        language='en',
        timezone='UTC',
        dashboard_layout='grid',
        items_per_page=20
    )


@pytest.fixture
def feature_toggle(db):
    """Create a test feature toggle"""
    return FeatureToggle.objects.create(
        name='Test Feature',
        description='Test Feature Description',
        category='ui',
        is_enabled=True,
        is_global=False
    )


@pytest.fixture
def system_setting(db):
    """Create a test system setting"""
    return SystemSettings.objects.create(
        key='test_setting',
        value='test_value',
        description='Test Setting',
        category='general',
        data_type='string'
    )


@pytest.fixture
def csv_file_content():
    """Generate CSV file content for testing"""
    return """first_name,last_name,email,phone,company,industry,country
John,Doe,john.doe@example.com,+1234567890,Example Corp,Technology,USA
Jane,Smith,jane.smith@example.com,+1234567891,Test Inc,Finance,Canada
Bob,Johnson,bob.johnson@example.com,+1234567892,Sample LLC,Healthcare,UK
"""


@pytest.fixture
def csv_file(csv_file_content):
    """Create a temporary CSV file"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    temp_file.write(csv_file_content)
    temp_file.close()
    yield temp_file.name
    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def csv_file_object(csv_file_content):
    """Create a CSV file object for upload"""
    file_obj = BytesIO(csv_file_content.encode('utf-8'))
    file_obj.name = 'test_contacts.csv'
    return file_obj


@pytest.fixture
def mock_supabase():
    """Mock Supabase client"""
    with patch('supabase.create_client') as mock_create:
        mock_client = Mock()
        mock_auth = Mock()
        mock_response = Mock()
        mock_user = Mock()
        mock_session = Mock()
        
        mock_user.id = 'test-user-id'
        mock_user.email = 'test@example.com'
        mock_user.email_confirmed_at = None
        mock_user.user_metadata = {}
        
        mock_session.access_token = 'test-access-token'
        mock_session.refresh_token = 'test-refresh-token'
        
        mock_response.user = mock_user
        mock_response.session = mock_session
        
        mock_auth.sign_in_with_password = Mock(return_value=mock_response)
        mock_auth.sign_up = Mock(return_value=mock_response)
        mock_auth.reset_password_for_email = Mock(return_value=None)
        mock_auth.refresh_session = Mock(return_value=mock_response)
        
        mock_client.auth = mock_auth
        mock_create.return_value = mock_client
        
        yield mock_client


@pytest.fixture
def mock_celery():
    """Mock Celery task execution"""
    with patch('apps.imports.tasks.process_import_task.delay') as mock_import, \
         patch('apps.exports.tasks.process_export_task.delay') as mock_export:
        yield {
            'import': mock_import,
            'export': mock_export
        }


@pytest.fixture
def mock_playwright():
    """Mock Playwright for job scraper tests"""
    with patch('playwright.async_api.async_playwright') as mock_playwright_module:
        mock_browser = Mock()
        mock_page = Mock()
        mock_context = Mock()
        
        mock_page.goto = Mock()
        mock_page.locator = Mock(return_value=Mock(click=Mock(), count=Mock(return_value=0)))
        mock_page.query_selector_all = Mock(return_value=[])
        mock_page.wait_for_timeout = Mock()
        mock_page.evaluate = Mock(return_value=[])
        
        mock_context.new_page = Mock(return_value=mock_page)
        mock_browser.new_context = Mock(return_value=mock_context)
        mock_browser.close = Mock()
        
        mock_playwright_instance = Mock()
        mock_playwright_instance.chromium = Mock()
        mock_playwright_instance.chromium.launch = Mock(return_value=mock_browser)
        
        mock_playwright_module.return_value.__aenter__ = Mock(return_value=mock_playwright_instance)
        mock_playwright_module.return_value.__aexit__ = Mock()
        
        yield {
            'playwright': mock_playwright_module,
            'browser': mock_browser,
            'page': mock_page
        }


@pytest.fixture(autouse=True)
def disable_logging():
    """Disable logging during tests"""
    import logging
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def media_root(tmp_path):
    """Temporary media root for file uploads"""
    media_path = tmp_path / 'media'
    media_path.mkdir()
    settings.MEDIA_ROOT = str(media_path)
    yield media_path
    # Cleanup handled by tmp_path


@pytest.fixture
def temp_data_dir(tmp_path):
    """Temporary directory for test data files"""
    data_dir = tmp_path / 'data'
    data_dir.mkdir()
    return data_dir

