"""
Tests for accounts app - Authentication, User Management
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AdminUserModelTestCase(TestCase):
    """Test cases for AdminUser model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            name="Test User"
        )
    
    def test_user_creation(self):
        """Test creating a user"""
        self.assertIsNotNone(self.user.id)
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.name, "Test User")
    
    def test_user_str_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), "Test User (test@example.com)")
    
    def test_can_export_property(self):
        """Test can_export property"""
        self.assertTrue(self.user.can_export)
    
    def test_download_limit(self):
        """Test download limit decrement"""
        initial_limit = self.user.download_limit
        self.user.decrement_download_limit()
        self.assertEqual(self.user.download_limit, initial_limit - 1)
    
    def test_role_default(self):
        """Test default role"""
        new_user = User.objects.create_user(
            username="newuser",
            email="new@example.com",
            password="pass123"
        )
        self.assertEqual(new_user.role, 'user')


class AuthenticationTestCase(TestCase):
    """Test cases for authentication views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            name="Test User"
        )
    
    def test_login_page_loads(self):
        """Test login page loads"""
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(reverse('admin:login'), {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
    
    def test_login_failure(self):
        """Test failed login"""
        response = self.client.post(reverse('admin:login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stays on page
    
    def test_logout(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('admin:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout


class ProfileTestCase(TestCase):
    """Test cases for profile management"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            name="Test User"
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_profile(self):
        """Test retrieving profile"""
        response = self.client.get('/api/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_profile(self):
        """Test updating profile"""
        data = {
            'name': 'Updated Name',
            'email': 'updated@example.com'
        }
        response = self.client.put('/api/api/profile/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')


class PasswordResetTestCase(TestCase):
    """Test cases for password reset"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_forgot_password_page_loads(self):
        """Test forgot password page loads"""
        response = self.client.get(reverse('admin:forgot_password'))
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_request(self):
        """Test password reset request"""
        response = self.client.post(reverse('admin:post_forgot_password'), {
            'email': 'test@example.com'
        })
        # Should redirect or show success message
        self.assertIn(response.status_code, [200, 302])

