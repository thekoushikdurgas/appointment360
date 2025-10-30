"""
Contact Service - Business logic for contacts
Migrated from Stremlit/services/contact_service.py
"""
import re
from typing import Optional, Dict, List
from django.db.models import Q, Count, F
from apps.contacts.models import Contact


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone format"""
    pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'
    return re.match(pattern, phone) is not None


def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://.+'
    return re.match(pattern, url) is not None


class ContactService:
    """Contact service for Django"""
    
    @staticmethod
    def create_contact(contact_data: Dict) -> Contact:
        """Create a new contact"""
        # Validate email
        if 'email' in contact_data and contact_data['email']:
            if not validate_email(contact_data['email']):
                raise ValueError("Invalid email format")
        
        # Validate phone
        if 'phone' in contact_data and contact_data['phone']:
            if not validate_phone(contact_data['phone']):
                raise ValueError("Invalid phone format")
        
        # Combine first and last name
        full_name = f"{contact_data.get('first_name', '')} {contact_data.get('last_name', '')}".strip()
        contact_data['full_name'] = full_name
        
        # Remove None values
        contact_data = {k: v for k, v in contact_data.items() if v is not None and v != ''}
        
        contact = Contact(**contact_data)
        contact.save()
        return contact
    
    @staticmethod
    def get_contact(contact_id: int) -> Optional[Contact]:
        """Get contact by ID"""
        try:
            return Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            return None
    
    @staticmethod
    def get_contact_by_email(email: str) -> Optional[Contact]:
        """Get contact by email"""
        try:
            return Contact.objects.get(email=email)
        except Contact.DoesNotExist:
            return None
    
    @staticmethod
    def update_contact(contact_id: int, contact_data: Dict) -> Optional[Contact]:
        """Update contact"""
        contact = ContactService.get_contact(contact_id)
        if not contact:
            return None
        
        # Validate email if changed
        if 'email' in contact_data and contact_data['email'] != contact.email:
            if not validate_email(contact_data['email']):
                raise ValueError("Invalid email format")
        
        # Validate phone if changed
        if 'phone' in contact_data and contact_data['phone'] != contact.phone:
            if not validate_phone(contact_data['phone']):
                raise ValueError("Invalid phone format")
        
        # Update full_name if names changed
        if 'first_name' in contact_data or 'last_name' in contact_data:
            contact_data['full_name'] = f"{contact_data.get('first_name', contact.first_name)} {contact_data.get('last_name', contact.last_name)}".strip()
        
        # Remove None values
        contact_data = {k: v for k, v in contact_data.items() if v is not None}
        
        for key, value in contact_data.items():
            if hasattr(contact, key):
                setattr(contact, key, value)
        
        contact.save()
        return contact
    
    @staticmethod
    def delete_contact(contact_id: int) -> bool:
        """Delete contact"""
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.delete()
            return True
        except Contact.DoesNotExist:
            return False
    
    @staticmethod
    def search_contacts(query: str, limit: int = 100) -> List[Contact]:
        """Search contacts by name, company, email"""
        return Contact.objects.filter(
            Q(full_name__icontains=query) |
            Q(company__icontains=query) |
            Q(email__icontains=query) |
            Q(title__icontains=query)
        )[:limit]
    
    @staticmethod
    def filter_contacts(filters: Dict, page: int = 1, per_page: int = 25) -> Dict:
        """Filter contacts with pagination"""
        query = Contact.objects.all()
        
        # Apply filters
        if filters.get('search'):
            search = filters['search']
            query = query.filter(
                Q(full_name__icontains=search) |
                Q(company__icontains=search) |
                Q(email__icontains=search)
            )
        
        if filters.get('industry'):
            query = query.filter(industry__in=filters['industry'])
        
        if filters.get('country'):
            query = query.filter(country__in=filters['country'])
        
        if filters.get('city'):
            query = query.filter(city__icontains=filters['city'])
        
        # Count total
        total = query.count()
        
        # Paginate
        offset = (page - 1) * per_page
        contacts = list(query.order_by('-created_at')[offset:offset + per_page])
        
        return {
            'contacts': contacts,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def get_contact_stats() -> Dict:
        """Get contact statistics"""
        total = Contact.objects.count()
        active = Contact.objects.filter(is_active=True).count()
        
        industries = Contact.objects.values('industry').distinct().count()
        countries = Contact.objects.values('country').distinct().count()
        
        return {
            'total': total,
            'active': active,
            'industries': industries,
            'countries': countries
        }
    
    @staticmethod
    def get_industry_distribution(limit: int = 10) -> List[Dict]:
        """Get industry distribution"""
        return list(Contact.objects.filter(industry__isnull=False).values('industry').annotate(
            count=Count('id')
        ).order_by('-count')[:limit])
    
    @staticmethod
    def get_country_distribution(limit: int = 10) -> List[Dict]:
        """Get country distribution"""
        return list(Contact.objects.filter(country__isnull=False).values('country').annotate(
            count=Count('id')
        ).order_by('-count')[:limit])

