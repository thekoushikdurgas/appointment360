"""
Tests for accounts models
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test User model"""
    
    def test_user_creation(self, user):
        """Test user can be created"""
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.is_active is True
        assert user.check_password('testpass123')
    
    def test_user_full_name(self, user):
        """Test user full name method"""
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.save()
        
        assert user.get_full_name() == 'John Doe'
        assert user.get_full_name() != 'testuser'
    
    def test_user_str_method(self, user):
        """Test user string representation"""
        assert str(user) in ['test@example.com', 'testuser']
    
    def test_user_profile_picture_url(self, user):
        """Test profile picture URL generation"""
        url = user.get_profile_picture_url()
        assert url is not None
        assert isinstance(url, str)
        
        # Test with custom profile picture
        user.profile_picture = 'https://example.com/pic.jpg'
        user.save()
        assert user.get_profile_picture_url() == 'https://example.com/pic.jpg'
    
    def test_user_supabase_fields(self, db):
        """Test Supabase-related fields"""
        user = User.objects.create_user(
            username='supabase_user',
            email='supabase@example.com',
            password='pass123',
            supabase_user_id='test-supabase-id',
            supabase_email='supabase@example.com'
        )
        
        assert user.supabase_user_id == 'test-supabase-id'
        assert user.supabase_email == 'supabase@example.com'
    
    def test_user_role_choices(self, db):
        """Test user role field"""
        user = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='pass123',
            role='manager'
        )
        
        assert user.role == 'manager'
    
    def test_user_email_verification(self, db):
        """Test email verification status"""
        user = User.objects.create_user(
            username='unverified',
            email='unverified@example.com',
            password='pass123',
            email_verified=False
        )
        
        assert user.email_verified is False
        
        user.email_verified = True
        user.save()
        assert user.email_verified is True

