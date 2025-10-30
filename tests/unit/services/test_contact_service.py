"""
Tests for contact service
"""
import pytest
from services.contact_service import ContactService, validate_email, validate_phone, validate_url
from apps.contacts.models import Contact


@pytest.mark.django_db
class TestContactServiceValidation:
    """Test validation functions"""
    
    def test_validate_email_valid(self):
        """Test valid email validation"""
        assert validate_email('test@example.com') is True
        assert validate_email('user.name@domain.co.uk') is True
    
    def test_validate_email_invalid(self):
        """Test invalid email validation"""
        assert validate_email('invalid-email') is False
        assert validate_email('@example.com') is False
        assert validate_email('test@') is False
    
    def test_validate_phone_valid(self):
        """Test valid phone validation"""
        assert validate_phone('+1234567890') is True
        assert validate_phone('(123) 456-7890') is True
        assert validate_phone('123-456-7890') is True
    
    def test_validate_phone_invalid(self):
        """Test invalid phone validation"""
        assert validate_phone('abc') is False
        assert validate_phone('123') is False  # Too short
    
    def test_validate_url_valid(self):
        """Test valid URL validation"""
        assert validate_url('https://example.com') is True
        assert validate_url('http://test.com/path') is True
    
    def test_validate_url_invalid(self):
        """Test invalid URL validation"""
        assert validate_url('not-a-url') is False
        assert validate_url('example.com') is False  # Missing protocol


@pytest.mark.django_db
class TestContactServiceMethods:
    """Test ContactService methods"""
    
    def test_create_contact(self, db):
        """Test create contact"""
        contact_data = {
            'first_name': 'New',
            'last_name': 'Contact',
            'email': 'newcontact@example.com',
            'phone': '+1234567890',
            'company': 'Test Corp'
        }
        contact = ContactService.create_contact(contact_data)
        assert contact.id is not None
        assert contact.full_name == 'New Contact'
    
    def test_create_contact_invalid_email(self, db):
        """Test create contact with invalid email"""
        contact_data = {
            'first_name': 'Test',
            'email': 'invalid-email',
            'phone': '+1234567890'
        }
        with pytest.raises(ValueError):
            ContactService.create_contact(contact_data)
    
    def test_get_contact(self, contact):
        """Test get contact by ID"""
        retrieved = ContactService.get_contact(contact.id)
        assert retrieved is not None
        assert retrieved.id == contact.id
    
    def test_get_contact_not_found(self, db):
        """Test get non-existent contact"""
        retrieved = ContactService.get_contact(99999)
        assert retrieved is None
    
    def test_update_contact(self, contact):
        """Test update contact"""
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        updated = ContactService.update_contact(contact.id, updated_data)
        assert updated is not None
        assert updated.first_name == 'Updated'
    
    def test_delete_contact(self, contact):
        """Test delete contact"""
        contact_id = contact.id
        result = ContactService.delete_contact(contact_id)
        assert result is True
        assert not Contact.objects.filter(id=contact_id).exists()
    
    def test_search_contacts(self, multiple_contacts):
        """Test search contacts"""
        results = ContactService.search_contacts('User', limit=5)
        assert len(results) > 0
    
    def test_get_contact_stats(self, multiple_contacts):
        """Test get contact statistics"""
        stats = ContactService.get_contact_stats()
        assert 'total' in stats
        assert 'active' in stats
        assert 'industries' in stats
        assert 'countries' in stats
    
    def test_get_industry_distribution(self, multiple_contacts):
        """Test get industry distribution"""
        distribution = ContactService.get_industry_distribution(limit=5)
        assert isinstance(distribution, list)
    
    def test_get_country_distribution(self, multiple_contacts):
        """Test get country distribution"""
        distribution = ContactService.get_country_distribution(limit=5)
        assert isinstance(distribution, list)

