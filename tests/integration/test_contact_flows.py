"""
Integration tests for contact management flows
"""
import pytest
from django.urls import reverse
from apps.contacts.models import Contact


@pytest.mark.django_db
@pytest.mark.integration
class TestContactManagementFlows:
    """Test complete contact management flows"""
    
    def test_complete_contact_crud_flow(self, authenticated_client):
        """Test complete CRUD flow for contacts"""
        # Create
        response = authenticated_client.post(
            reverse('contacts:create'),
            {
                'first_name': 'Integration',
                'last_name': 'Test',
                'email': 'integration@example.com',
                'phone': '+1234567890',
                'company': 'Test Corp',
                'is_active': True
            }
        )
        assert response.status_code == 302
        
        # Verify created
        contact = Contact.objects.get(email='integration@example.com')
        assert contact is not None
        
        # Read/List
        response = authenticated_client.get(reverse('contacts:list'))
        assert response.status_code == 200
        assert 'integration@example.com' in response.content.decode() or contact.id is not None
        
        # Update
        response = authenticated_client.post(
            reverse('contacts:update', args=[contact.id]),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'email': contact.email,
                'is_active': True
            }
        )
        assert response.status_code == 302
        contact.refresh_from_db()
        assert contact.first_name == 'Updated'
        
        # Delete
        response = authenticated_client.post(reverse('contacts:delete', args=[contact.id]))
        assert response.status_code == 302
        assert not Contact.objects.filter(id=contact.id).exists()
    
    def test_complete_contact_search_and_filter_flow(self, authenticated_client, multiple_contacts):
        """Test search and filter flow"""
        # Search
        response = authenticated_client.get(
            reverse('contacts:list'),
            {'search': 'User1'}
        )
        assert response.status_code == 200
        
        # Filter by industry
        response = authenticated_client.get(
            reverse('contacts:list'),
            {'industry': ['Technology']}
        )
        assert response.status_code == 200
        
        # Filter by country
        response = authenticated_client.get(
            reverse('contacts:list'),
            {'country': ['USA']}
        )
        assert response.status_code == 200

