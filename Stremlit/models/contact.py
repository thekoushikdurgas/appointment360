"""
Contact Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base


class Contact(Base):
    """Contact model with comprehensive fields"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Information
    full_name = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)
    email = Column(String, index=True)
    phone = Column(String)
    
    # Company Information
    company = Column(String, index=True)
    industry = Column(String, index=True)
    company_size = Column(String)
    company_address = Column(Text)
    website = Column(String)
    
    # Extended Company Fields
    employees_count = Column(Integer)  # Number of employees
    annual_revenue = Column(Integer)  # Annual revenue in dollars
    total_funding = Column(Integer)  # Total funding raised
    latest_funding_amount = Column(Integer)  # Latest funding amount
    
    # Additional Person Fields
    seniority = Column(String)  # Job seniority level
    departments = Column(Text)  # Department(s) - comma separated
    keywords = Column(Text)  # Keywords/tags
    technologies = Column(Text)  # Technologies used
    email_status = Column(String)  # Email verification status
    stage = Column(String)  # Lead stage (Cold, Warm, Hot)
    
    # Location
    city = Column(String, index=True)
    state = Column(String, index=True)
    country = Column(String, index=True)
    postal_code = Column(String)
    
    # Company Location
    company_city = Column(String)
    company_state = Column(String)
    company_country = Column(String)
    company_phone = Column(String)
    
    # Social Media
    linkedin = Column(String)
    person_linkedin_url = Column(String)
    company_linkedin_url = Column(String)
    facebook_url = Column(String)
    facebook = Column(String)  # Keep for backward compatibility
    twitter_url = Column(String)
    twitter = Column(String)  # Keep for backward compatibility
    
    # Additional Fields
    notes = Column(Text)
    tags = Column(String)
    status = Column(String, default="active")
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User tracking
    user_id = Column(String, nullable=True)  # UUID string from Supabase
    
    def __repr__(self):
        return f"<Contact {self.full_name} ({self.email})>"

