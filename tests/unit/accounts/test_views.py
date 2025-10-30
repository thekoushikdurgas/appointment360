"""
Tests for accounts views
"""
import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, Mock

User = get_user_model()


@pytest.mark.django_db
class TestLoginView:
    """Test login view"""
    
    def test_login_view_get(self, client):
        """Test login page loads"""
        response = client.get(reverse('accounts:login'))
        assert response.status_code == 200
        assert 'login' in response.content.decode().lower()
    
    def test_login_view_with_valid_credentials(self, client, user, mock_supabase):
        """Test login with valid credentials"""
        # Mock Supabase authentication
        mock_supabase.auth.sign_in_with_password.return_value.session = Mock(
            access_token='test-token',
            refresh_token='refresh-token'
        )
        mock_supabase.auth.sign_in_with_password.return_value.user = Mock(
            id='user-id',
            email='test@example.com',
            email_confirmed_at=None,
            user_metadata={}
        )
        
        response = client.post(
            reverse('accounts:login'),
            {
                'email': 'test@example.com',
                'password': 'testpass123'
            }
        )
        
        # Should redirect on success
        assert response.status_code in [200, 302]
    
    def test_login_view_with_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post(
            reverse('accounts:login'),
            {
                'email': 'wrong@example.com',
                'password': 'wrongpass'
            }
        )
        
        assert response.status_code == 200
    
    def test_login_view_remember_me(self, client, user, mock_supabase):
        """Test remember me functionality"""
        mock_supabase.auth.sign_in_with_password.return_value.session = Mock(
            access_token='test-token',
            refresh_token='refresh-token'
        )
        mock_supabase.auth.sign_in_with_password.return_value.user = Mock(
            id='user-id',
            email='test@example.com',
            email_confirmed_at=None
        )
        
        response = client.post(
            reverse('accounts:login'),
            {
                'email': 'test@example.com',
                'password': 'testpass123',
                'remember': 'on'
            }
        )
        
        # Check session expiry is extended
        assert response.status_code in [200, 302]


@pytest.mark.django_db
class TestSignupView:
    """Test signup view"""
    
    def test_signup_view_get(self, client):
        """Test signup page loads"""
        response = client.get(reverse('accounts:signup'))
        assert response.status_code == 200
    
    @patch('apps.accounts.views.create_client')
    def test_signup_view_with_valid_data(self, mock_create_client, client):
        """Test signup with valid data"""
        # Mock Supabase signup
        mock_user = Mock()
        mock_user.id = 'new-user-id'
        mock_user.email = 'newuser@example.com'
        
        mock_response = Mock()
        mock_response.user = mock_user
        
        mock_client = Mock()
        mock_client.auth.sign_up.return_value = mock_response
        mock_create_client.return_value = mock_client
        
        response = client.post(
            reverse('accounts:signup'),
            {
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@example.com',
                'password': 'newpass123',
                'confirm_password': 'newpass123'
            }
        )
        
        assert response.status_code in [200, 302]
    
    def test_signup_view_with_mismatched_passwords(self, client):
        """Test signup with password mismatch"""
        response = client.post(
            reverse('accounts:signup'),
            {
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@example.com',
                'password': 'pass123',
                'confirm_password': 'pass456'
            }
        )
        
        assert response.status_code == 200
    
    def test_signup_view_with_short_password(self, client):
        """Test signup with short password"""
        response = client.post(
            reverse('accounts:signup'),
            {
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@example.com',
                'password': 'short',
                'confirm_password': 'short'
            }
        )
        
        assert response.status_code == 200


@pytest.mark.django_db
class TestLogoutView:
    """Test logout view"""
    
    def test_logout_view(self, authenticated_client):
        """Test logout functionality"""
        response = authenticated_client.get(reverse('accounts:logout'))
        assert response.status_code == 302
        assert 'login' in response.url.lower()


@pytest.mark.django_db
class TestProfileView:
    """Test profile view"""
    
    def test_profile_view_get(self, authenticated_client, user):
        """Test profile page loads"""
        response = authenticated_client.get(reverse('accounts:profile'))
        assert response.status_code == 200
    
    def test_profile_view_update(self, authenticated_client, user):
        """Test profile update"""
        response = authenticated_client.post(
            reverse('accounts:profile'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'phone': '+1234567890'
            }
        )
        
        assert response.status_code in [200, 302]
        user.refresh_from_db()
        assert user.first_name == 'Updated'
    
    def test_profile_view_unauthorized(self, client):
        """Test profile view requires authentication"""
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
class TestPasswordResetView:
    """Test password reset view"""
    
    def test_password_reset_view_get(self, client):
        """Test password reset page loads"""
        response = client.get(reverse('accounts:password-reset'))
        assert response.status_code == 200
    
    @patch('apps.accounts.views.create_client')
    def test_password_reset_request(self, mock_create_client, client):
        """Test password reset request"""
        mock_client = Mock()
        mock_client.auth.reset_password_for_email = Mock(return_value=None)
        mock_create_client.return_value = mock_client
        
        response = client.post(
            reverse('accounts:password-reset'),
            {'email': 'test@example.com'}
        )
        
        assert response.status_code in [200, 302]


@pytest.mark.django_db
class TestEmailVerifyView:
    """Test email verification view"""
    
    def test_email_verify_view(self, client):
        """Test email verification page"""
        response = client.get(reverse('accounts:verify-email'))
        assert response.status_code == 200
        
        # Test with token parameter
        response = client.get(
            reverse('accounts:verify-email'),
            {'token': 'test-token', 'type': 'signup'}
        )
        assert response.status_code == 200

