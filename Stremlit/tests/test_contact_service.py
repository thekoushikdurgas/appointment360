"""
Tests for Contact Service
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.contact_service import ContactService
from models.contact import Contact
from config.database import Base


@pytest.fixture
def test_db():
    """Create test database"""
    # Use PostgreSQL test database
    from config.settings import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_contact(test_db):
    """Test creating a contact"""
    service = ContactService(test_db)
    
    contact_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'full_name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
        'company': 'Test Company',
        'industry': 'Technology',
        'user_id': 1
    }
    
    contact = service.create_contact(contact_data)
    
    assert contact is not None
    assert contact.email == 'john.doe@example.com'
    assert contact.full_name == 'John Doe'


def test_get_contact(test_db):
    """Test getting a contact by ID"""
    service = ContactService(test_db)
    
    # Create contact
    contact_data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'full_name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'phone': '+1234567891',
        'company': 'Test Company',
        'industry': 'Technology',
        'user_id': 1
    }
    
    created = service.create_contact(contact_data)
    
    # Retrieve contact
    retrieved = service.get_contact(created.id)
    
    assert retrieved is not None
    assert retrieved.email == 'jane.smith@example.com'


def test_get_contact_by_email(test_db):
    """Test getting a contact by email"""
    service = ContactService(test_db)
    
    contact_data = {
        'first_name': 'Bob',
        'last_name': 'Johnson',
        'full_name': 'Bob Johnson',
        'email': 'bob.johnson@example.com',
        'phone': '+1234567892',
        'company': 'Test Company',
        'industry': 'Technology',
        'user_id': 1
    }
    
    service.create_contact(contact_data)
    
    # Get by email
    retrieved = service.get_contact_by_email('bob.johnson@example.com')
    
    assert retrieved is not None
    assert retrieved.email == 'bob.johnson@example.com'


def test_update_contact(test_db):
    """Test updating a contact"""
    service = ContactService(test_db)
    
    # Create contact
    contact_data = {
        'first_name': 'Alice',
        'last_name': 'Brown',
        'full_name': 'Alice Brown',
        'email': 'alice.brown@example.com',
        'phone': '+1234567893',
        'company': 'Test Company',
        'industry': 'Technology',
        'user_id': 1
    }
    
    created = service.create_contact(contact_data)
    
    # Update contact
    update_data = {
        'first_name': 'Alice',
        'last_name': 'Green',
        'full_name': 'Alice Green',
        'email': 'alice.green@example.com',
        'company': 'New Company'
    }
    
    updated = service.update_contact(created.id, update_data)
    
    assert updated is not None
    assert updated.last_name == 'Green'
    assert updated.company == 'New Company'


def test_delete_contact(test_db):
    """Test deleting a contact"""
    service = ContactService(test_db)
    
    # Create contact
    contact_data = {
        'first_name': 'Charlie',
        'last_name': 'Davis',
        'full_name': 'Charlie Davis',
        'email': 'charlie.davis@example.com',
        'phone': '+1234567894',
        'company': 'Test Company',
        'industry': 'Technology',
        'user_id': 1
    }
    
    created = service.create_contact(contact_data)
    contact_id = created.id
    
    # Delete contact
    result = service.delete_contact(contact_id)
    
    assert result is True
    
    # Verify deletion
    retrieved = service.get_contact(contact_id)
    assert retrieved is None


def test_filter_contacts(test_db):
    """Test filtering contacts"""
    service = ContactService(test_db)
    
    # Create multiple contacts
    contacts = [
        {
            'first_name': 'David',
            'last_name': 'Wilson',
            'full_name': 'David Wilson',
            'email': 'david.wilson@tech.com',
            'phone': '+1234567895',
            'company': 'Tech Corp',
            'industry': 'Technology',
            'country': 'USA',
            'user_id': 1
        },
        {
            'first_name': 'Emily',
            'last_name': 'Martinez',
            'full_name': 'Emily Martinez',
            'email': 'emily.martinez@health.com',
            'phone': '+1234567896',
            'company': 'Health Inc',
            'industry': 'Healthcare',
            'country': 'USA',
            'user_id': 1
        }
    ]
    
    for contact_data in contacts:
        service.create_contact(contact_data)
    
    # Filter by industry
    result = service.filter_contacts({'industry': ['Technology']})
    
    assert result['total'] == 1
    assert result['contacts'][0].industry == 'Technology'


def test_get_contact_stats(test_db):
    """Test getting contact statistics"""
    service = ContactService(test_db)
    
    # Create contacts
    contacts = [
        {
            'first_name': 'Frank',
            'last_name': 'Anderson',
            'full_name': 'Frank Anderson',
            'email': 'frank.anderson@example.com',
            'phone': '+1234567897',
            'company': 'Test Corp',
            'industry': 'Technology',
            'user_id': 1,
            'is_active': True
        },
        {
            'first_name': 'Grace',
            'last_name': 'Lee',
            'full_name': 'Grace Lee',
            'email': 'grace.lee@example.com',
            'phone': '+1234567898',
            'company': 'Test Corp',
            'industry': 'Finance',
            'user_id': 1,
            'is_active': True
        },
        {
            'first_name': 'Henry',
            'last_name': 'Taylor',
            'full_name': 'Henry Taylor',
            'email': 'henry.taylor@example.com',
            'phone': '+1234567899',
            'company': 'Test Corp',
            'industry': 'Technology',
            'user_id': 1,
            'is_active': False
        }
    ]
    
    for contact_data in contacts:
        service.create_contact(contact_data)
    
    stats = service.get_contact_stats()
    
    assert stats['total'] == 3
    assert stats['active'] == 2
    assert stats['industries'] == 2  # Technology, Finance


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

