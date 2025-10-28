"""
Contact Service - CRUD operations for contacts
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from typing import List, Optional, Dict
from models.contact import Contact
from datetime import datetime
from utils.validators import validate_email, validate_phone


class ContactService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_contact(self, contact_data: Dict) -> Contact:
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
        
        contact = Contact(**contact_data)
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact
    
    def get_contact(self, contact_id: int) -> Optional[Contact]:
        """Get contact by ID"""
        return self.db.query(Contact).filter(Contact.id == contact_id).first()
    
    def get_contact_by_email(self, email: str) -> Optional[Contact]:
        """Get contact by email"""
        return self.db.query(Contact).filter(Contact.email == email).first()
    
    def update_contact(self, contact_id: int, contact_data: Dict) -> Optional[Contact]:
        """Update contact"""
        contact = self.get_contact(contact_id)
        if not contact:
            return None
        
        # Update fields
        for key, value in contact_data.items():
            if hasattr(contact, key):
                setattr(contact, key, value)
        
        contact.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(contact)
        return contact
    
    def delete_contact(self, contact_id: int) -> bool:
        """Delete contact"""
        contact = self.get_contact(contact_id)
        if not contact:
            return False
        
        self.db.delete(contact)
        self.db.commit()
        return True
    
    def search_contacts(self, query: str, limit: int = 100) -> List[Contact]:
        """Search contacts by name, company, email"""
        search_filter = or_(
            Contact.full_name.ilike(f"%{query}%"),
            Contact.company.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%"),
            Contact.title.ilike(f"%{query}%")
        )
        return self.db.query(Contact).filter(search_filter).limit(limit).all()
    
    def filter_contacts(self, filters: Dict, page: int = 1, per_page: int = 25) -> Dict:
        """Filter contacts with pagination"""
        query = self.db.query(Contact)
        
        # Apply filters
        if filters.get('search'):
            search = filters['search']
            query = query.filter(
                or_(
                    Contact.full_name.ilike(f"%{search}%"),
                    Contact.company.ilike(f"%{search}%"),
                    Contact.email.ilike(f"%{search}%")
                )
            )
        
        if filters.get('industry'):
            query = query.filter(Contact.industry.in_(filters['industry']))
        
        if filters.get('country'):
            query = query.filter(Contact.country.in_(filters['country']))
        
        if filters.get('city'):
            query = query.filter(Contact.city.ilike(f"%{filters['city']}%"))
        
        # Count total
        total = query.count()
        
        # Paginate
        offset = (page - 1) * per_page
        contacts = query.order_by(desc(Contact.created_at)).offset(offset).limit(per_page).all()
        
        return {
            'contacts': contacts,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def get_contact_stats(self) -> Dict:
        """Get contact statistics"""
        total = self.db.query(Contact).count()
        active = self.db.query(Contact).filter(Contact.is_active == True).count()
        
        industries = self.db.query(Contact.industry).distinct().count()
        countries = self.db.query(Contact.country).distinct().count()
        
        return {
            'total': total,
            'active': active,
            'industries': industries,
            'countries': countries
        }
