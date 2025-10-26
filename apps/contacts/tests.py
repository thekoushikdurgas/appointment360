"""
Tests for Contact models and views
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Contact, Industry

User = get_user_model()


class ContactModelTestCase(TestCase):
    """Test cases for Contact model"""
    
    def setUp(self):
        """Set up test data"""
        self.industry = Industry.objects.create(
            name="Technology",
            description="Tech companies"
        )
    
    def test_contact_creation(self):
        """Test creating a contact"""
        contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company="Test Company",
            city="New York",
            country="USA"
        )
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertIsNotNone(contact.id)
    
    def test_full_name_property(self):
        """Test full_name property"""
        contact = Contact.objects.create(
            first_name="Jane",
            last_name="Smith"
        )
        self.assertEqual(contact.full_name, "Jane Smith")
    
    def test_location_property(self):
        """Test location property"""
        contact = Contact.objects.create(
            city="San Francisco",
            state="CA",
            country="USA"
        )
        self.assertEqual(contact.location, "San Francisco, CA, USA")


class ContactAPITestCase(TestCase):
    """Test cases for Contact API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test contacts
        Contact.objects.create(
            first_name="Alice",
            last_name="Johnson",
            email="alice@example.com",
            company="ABC Corp",
            city="Seattle",
            country="USA"
        )
    
    def test_list_contacts(self):
        """Test listing contacts"""
        response = self.client.get('/api/api/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_contact(self):
        """Test retrieving a contact"""
        contact = Contact.objects.first()
        response = self.client.get(f'/api/api/contacts/{contact.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Alice')
    
    def test_filter_contacts_by_city(self):
        """Test filtering contacts by city"""
        response = self.client.get('/api/api/contacts/?location=Seattle')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_create_contact(self):
        """Test creating a contact"""
        data = {
            'first_name': 'Bob',
            'last_name': 'Williams',
            'email': 'bob@example.com',
            'company': 'XYZ Inc',
            'city': 'Boston',
            'country': 'USA'
        }
        response = self.client.post('/api/api/contacts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.filter(email='bob@example.com').count(), 1)
    
    def test_autocomplete_search(self):
        """Test autocomplete functionality"""
        response = self.client.get('/api/api/contacts/autocomplete/?field=email&q=alice')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class IndustryTestCase(TestCase):
    """Test cases for Industry model"""
    
    def test_industry_creation(self):
        """Test creating an industry"""
        industry = Industry.objects.create(
            name="Healthcare",
            description="Healthcare sector"
        )
        self.assertEqual(industry.name, "Healthcare")
        self.assertTrue(industry.is_active)

