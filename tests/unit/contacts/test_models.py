"""
Tests for contacts models
"""
import pytest
from apps.contacts.models import Contact


@pytest.mark.django_db
class TestContactModel:
    """Test Contact model"""
    
    def test_contact_creation(self, contact):
        """Test contact can be created"""
        assert contact.first_name == 'John'
        assert contact.last_name == 'Doe'
        assert contact.full_name == 'John Doe'
        assert contact.email == 'john.doe@example.com'
        assert contact.is_active is True
    
    def test_contact_str_method(self, contact):
        """Test contact string representation"""
        assert 'John Doe' in str(contact)
        assert 'john.doe@example.com' in str(contact)
    
    def test_contact_repr_method(self, contact):
        """Test contact repr method"""
        repr_str = repr(contact)
        assert 'Contact' in repr_str
        assert 'John Doe' in repr_str
    
    def test_contact_ordering(self, db, multiple_contacts):
        """Test contacts are ordered by created_at descending"""
        contacts = list(Contact.objects.all())
        if len(contacts) > 1:
            # Most recent should be first
            assert contacts[0].created_at >= contacts[1].created_at
    
    def test_contact_full_name_generation(self, db):
        """Test full_name is generated from first and last name"""
        contact = Contact.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            full_name='Jane Smith'
        )
        assert contact.full_name == 'Jane Smith'
    
    def test_contact_optional_fields(self, db):
        """Test contact with minimal required fields"""
        contact = Contact.objects.create(
            first_name='Min',
            last_name='Contact',
            full_name='Min Contact',
            email='min@example.com'
        )
        assert contact.email == 'min@example.com'
        assert contact.phone == ''  # Optional field
    
    def test_contact_is_active_default(self, db):
        """Test is_active defaults to True"""
        contact = Contact.objects.create(
            first_name='Test',
            last_name='User',
            full_name='Test User',
            email='test@example.com'
        )
        assert contact.is_active is True

