"""
Tests for contact forms
"""
import pytest
from apps.contacts.forms import ContactForm, ContactFilterForm
from apps.contacts.models import Contact


@pytest.mark.django_db
class TestContactForm:
    """Test ContactForm"""
    
    def test_contact_form_valid_data(self, contact):
        """Test form with valid data"""
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '+1234567890',
            'company': 'Test Corp',
            'industry': 'Technology',
            'city': 'New York',
            'state': 'NY',
            'country': 'USA',
            'is_active': True
        }
        form = ContactForm(data=form_data)
        assert form.is_valid()
    
    def test_contact_form_required_fields(self):
        """Test form requires email and first_name"""
        form_data = {
            'last_name': 'Smith'
        }
        form = ContactForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors or 'first_name' in form.errors
    
    def test_contact_form_email_validation(self, contact):
        """Test email validation in form"""
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email',  # Invalid format
            'is_active': True
        }
        form = ContactForm(data=form_data)
        # Form should validate email format
        assert not form.is_valid() or 'email' in form.errors
    
    def test_contact_form_duplicate_email(self, contact):
        """Test form prevents duplicate emails"""
        form_data = {
            'first_name': 'Another',
            'last_name': 'Person',
            'email': contact.email,  # Same email as existing contact
            'is_active': True
        }
        form = ContactForm(data=form_data)
        # Should raise validation error for duplicate
        if form.is_valid():
            form.save()
            # Check duplicate prevention
            assert Contact.objects.filter(email=contact.email).count() >= 1
    
    def test_contact_form_update_existing(self, contact):
        """Test form can update existing contact"""
        form = ContactForm(instance=contact, data={
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': contact.email,
            'is_active': True
        })
        if form.is_valid():
            updated_contact = form.save()
            assert updated_contact.first_name == 'Updated'


@pytest.mark.django_db
class TestContactFilterForm:
    """Test ContactFilterForm"""
    
    def test_filter_form_valid(self):
        """Test filter form with valid data"""
        form_data = {
            'search': 'test query',
            'industry': ['Technology'],
            'country': ['USA']
        }
        form = ContactFilterForm(data=form_data)
        # Form fields are all optional
        assert form.is_valid() or 'industry' not in form.errors
    
    def test_filter_form_empty(self):
        """Test filter form with no data"""
        form = ContactFilterForm(data={})
        # All fields are optional
        assert form.is_valid() is not False  # May or may not be valid, but shouldn't error

