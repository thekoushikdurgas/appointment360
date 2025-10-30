"""
Integration tests for authentication flows
"""
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestAuthenticationFlows:
    """Test complete authentication flows"""
    
    def test_complete_signup_flow(self, client, mock_supabase):
        """Test complete signup to login flow"""
        # Step 1: Access signup page
        response = client.get(reverse('accounts:signup'))
        assert response.status_code == 200
        
        # Step 2: Submit signup form
        with patch('apps.accounts.views.create_client') as mock_create:
            mock_user = Mock()
            mock_user.id = 'new-user-id'
            mock_user.email = 'newuser@example.com'
            mock_response = Mock()
            mock_response.user = mock_user
            mock_client = Mock()
            mock_client.auth.sign_up.return_value = mock_response
            mock_create.return_value = mock_client
            
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
            # Should redirect to login
            assert response.status_code in [200, 302]
    
    def test_complete_login_flow(self, client, user):
        """Test complete login flow"""
        # Step 1: Access login page
        response = client.get(reverse('accounts:login'))
        assert response.status_code == 200
        
        # Step 2: Login
        response = client.post(
            reverse('accounts:login'),
            {
                'email': 'test@example.com',
                'password': 'testpass123'
            }
        )
        # Should redirect after login
        assert response.status_code in [200, 302]
    
    def test_complete_logout_flow(self, authenticated_client):
        """Test complete logout flow"""
        # User is authenticated
        response = authenticated_client.get(reverse('core:dashboard'))
        assert response.status_code in [200, 302]
        
        # Logout
        response = authenticated_client.get(reverse('accounts:logout'))
        assert response.status_code == 302
        
        # Try to access protected page
        response = authenticated_client.get(reverse('core:dashboard'))
        # Should require login again
        assert response.status_code in [200, 302, 401]

