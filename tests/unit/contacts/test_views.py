"""
Tests for contacts views
"""
import pytest
import json
from django.urls import reverse
from apps.contacts.models import Contact


@pytest.mark.django_db
class TestContactListView:
    """Test contact list view"""
    
    def test_contact_list_view_get(self, authenticated_client, multiple_contacts):
        """Test contact list page loads"""
        response = authenticated_client.get(reverse('contacts:list'))
        assert response.status_code == 200
    
    def test_contact_list_view_pagination(self, authenticated_client, multiple_contacts):
        """Test contact list pagination"""
        response = authenticated_client.get(reverse('contacts:list'))
        assert response.status_code == 200
        # Should have pagination if more than 25 contacts
        if len(multiple_contacts) > 25:
            assert 'page' in response.content.decode().lower()
    
    def test_contact_list_view_search(self, authenticated_client, contact):
        """Test contact search functionality"""
        response = authenticated_client.get(
            reverse('contacts:list'),
            {'search': 'John'}
        )
        assert response.status_code == 200
        assert 'John' in response.content.decode() or response.context['contacts'].exists()
    
    def test_contact_list_view_filter_industry(self, authenticated_client, multiple_contacts):
        """Test industry filter"""
        response = authenticated_client.get(
            reverse('contacts:list'),
            {'industry': ['Technology']}
        )
        assert response.status_code == 200
    
    def test_contact_list_view_filter_country(self, authenticated_client, multiple_contacts):
        """Test country filter"""
        response = authenticated_client.get(
            reverse('contacts:list'),
            {'country': ['USA']}
        )
        assert response.status_code == 200
    
    def test_contact_list_view_requires_auth(self, client):
        """Test contact list requires authentication"""
        response = client.get(reverse('contacts:list'))
        assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
class TestContactCreateView:
    """Test contact create view"""
    
    def test_contact_create_view_get(self, authenticated_client):
        """Test contact create page loads"""
        response = authenticated_client.get(reverse('contacts:create'))
        assert response.status_code == 200
    
    def test_contact_create_view_post_valid(self, authenticated_client):
        """Test creating contact with valid data"""
        response = authenticated_client.post(
            reverse('contacts:create'),
            {
                'first_name': 'New',
                'last_name': 'Contact',
                'email': 'newcontact@example.com',
                'phone': '+1234567890',
                'company': 'New Corp',
                'is_active': True
            }
        )
        assert response.status_code == 302  # Redirect on success
        assert Contact.objects.filter(email='newcontact@example.com').exists()
    
    def test_contact_create_view_post_invalid(self, authenticated_client):
        """Test creating contact with invalid data"""
        response = authenticated_client.post(
            reverse('contacts:create'),
            {
                'first_name': 'New',
                'email': 'invalid-email'  # Invalid email
            }
        )
        # Should not redirect (form errors)
        assert response.status_code == 200


@pytest.mark.django_db
class TestContactUpdateView:
    """Test contact update view"""
    
    def test_contact_update_view_get(self, authenticated_client, contact):
        """Test contact update page loads"""
        response = authenticated_client.get(
            reverse('contacts:update', args=[contact.id])
        )
        assert response.status_code == 200
    
    def test_contact_update_view_post(self, authenticated_client, contact):
        """Test updating contact"""
        response = authenticated_client.post(
            reverse('contacts:update', args=[contact.id]),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'email': contact.email,
                'is_active': True
            }
        )
        assert response.status_code == 302  # Redirect on success
        contact.refresh_from_db()
        assert contact.first_name == 'Updated'
    
    def test_contact_update_view_not_found(self, authenticated_client):
        """Test updating non-existent contact"""
        response = authenticated_client.get(
            reverse('contacts:update', args=[99999])
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestContactDeleteView:
    """Test contact delete view"""
    
    def test_contact_delete_view_get(self, authenticated_client, contact):
        """Test contact delete confirmation page"""
        response = authenticated_client.get(
            reverse('contacts:delete', args=[contact.id])
        )
        assert response.status_code == 200
    
    def test_contact_delete_view_post(self, authenticated_client, contact):
        """Test deleting contact"""
        contact_id = contact.id
        response = authenticated_client.post(
            reverse('contacts:delete', args=[contact.id])
        )
        assert response.status_code == 302  # Redirect on success
        assert not Contact.objects.filter(id=contact_id).exists()
    
    def test_contact_delete_view_not_found(self, authenticated_client):
        """Test deleting non-existent contact"""
        response = authenticated_client.get(
            reverse('contacts:delete', args=[99999])
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestContactBulkOperations:
    """Test bulk operations"""
    
    def test_bulk_export_api(self, authenticated_client, multiple_contacts):
        """Test bulk export API"""
        contact_ids = [c.id for c in multiple_contacts[:3]]
        response = authenticated_client.post(
            reverse('contacts:bulk_export_api'),
            json.dumps({'contact_ids': contact_ids, 'format': 'csv'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
    
    def test_bulk_export_api_no_contacts(self, authenticated_client):
        """Test bulk export with no contacts selected"""
        response = authenticated_client.post(
            reverse('contacts:bulk_export_api'),
            json.dumps({'contact_ids': []}),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_bulk_delete_api(self, authenticated_client, multiple_contacts):
        """Test bulk delete API"""
        contact_ids = [c.id for c in multiple_contacts[:3]]
        response = authenticated_client.post(
            reverse('contacts:bulk_delete_api'),
            json.dumps({'contact_ids': contact_ids}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['success'] is True
    
    def test_bulk_update_api(self, authenticated_client, multiple_contacts):
        """Test bulk update API"""
        contact_ids = [c.id for c in multiple_contacts[:3]]
        response = authenticated_client.post(
            reverse('contacts:bulk_update_api'),
            json.dumps({
                'contact_ids': contact_ids,
                'field': 'industry',
                'value': 'Updated Industry'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['success'] is True

