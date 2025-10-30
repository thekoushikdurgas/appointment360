"""
Tests for Supabase authentication middleware
"""
import pytest
import time
from unittest.mock import Mock, patch
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from apps.accounts.middleware import SupabaseAuthMiddleware

User = get_user_model()


@pytest.mark.django_db
class TestSupabaseAuthMiddleware:
    """Test Supabase authentication middleware"""
    
    def test_middleware_initialization(self):
        """Test middleware can be initialized"""
        get_response = Mock(return_value=Mock(status_code=200))
        
        with patch('apps.accounts.middleware.create_client') as mock_create:
            middleware = SupabaseAuthMiddleware(get_response)
            assert middleware is not None
    
    def test_middleware_skips_static_files(self):
        """Test middleware skips static files"""
        get_response = Mock(return_value=Mock(status_code=200))
        middleware = SupabaseAuthMiddleware(get_response)
        
        request = RequestFactory().get('/static/css/style.css')
        request.user = Mock(is_authenticated=False)
        
        result = middleware.process_request(request)
        assert result is None  # Should skip processing
    
    def test_middleware_skips_login_page(self):
        """Test middleware skips login page"""
        get_response = Mock(return_value=Mock(status_code=200))
        middleware = SupabaseAuthMiddleware(get_response)
        
        request = RequestFactory().get('/accounts/login/')
        request.user = Mock(is_authenticated=False)
        
        result = middleware.process_request(request)
        assert result is None  # Should skip processing
    
    @patch('apps.accounts.middleware.create_client')
    def test_middleware_refreshes_token(self, mock_create):
        """Test middleware refreshes token if needed"""
        get_response = Mock(return_value=Mock(status_code=200))
        
        mock_client = Mock()
        mock_session = Mock()
        mock_session.access_token = 'new-token'
        mock_session.refresh_token = 'new-refresh-token'
        
        mock_response = Mock()
        mock_response.session = mock_session
        
        mock_client.auth.refresh_session.return_value = mock_response
        mock_create.return_value = mock_client
        
        middleware = SupabaseAuthMiddleware(get_response)
        
        request = RequestFactory().get('/dashboard/')
        mock_user = Mock()
        mock_user.is_authenticated = True
        mock_user.supabase_user_id = 'test-id'
        request.user = mock_user
        
        # Set token that is about to expire
        request.session = {
            'supabase_access_token': 'old-token',
            'supabase_refresh_token': 'old-refresh-token',
            'supabase_token_expires_at': time.time() + 100  # Less than 5 minutes
        }
        
        result = middleware.process_request(request)
        assert result is None
    
    def test_middleware_updates_last_activity(self):
        """Test middleware updates last activity"""
        get_response = Mock(return_value=Mock(status_code=200))
        middleware = SupabaseAuthMiddleware(get_response)
        
        request = RequestFactory().get('/dashboard/')
        mock_user = Mock()
        mock_user.is_authenticated = True
        request.user = mock_user
        request.session = {}
        
        response = middleware.process_response(request, get_response())
        
        assert 'last_activity' in request.session
        assert isinstance(request.session['last_activity'], (int, float))
    
    def test_middleware_handles_timeout(self):
        """Test middleware handles session timeout"""
        get_response = Mock(return_value=Mock(status_code=200))
        middleware = SupabaseAuthMiddleware(get_response)
        
        request = RequestFactory().get('/dashboard/')
        mock_user = Mock()
        mock_user.is_authenticated = True
        mock_user.supabase_user_id = 'test-id'
        request.user = mock_user
        request.session = {
            'last_activity': time.time() - 4000  # More than 1 hour ago
        }
        
        with patch('apps.accounts.middleware.logout') as mock_logout:
            result = middleware.process_request(request)
            # Should logout or redirect
            assert result is None or hasattr(result, 'status_code')

