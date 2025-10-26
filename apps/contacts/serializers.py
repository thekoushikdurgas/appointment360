"""
Serializers for Contact model
"""
from rest_framework import serializers
from .models import Contact, Industry


class IndustrySerializer(serializers.ModelSerializer):
    """Serializer for Industry model"""
    
    class Meta:
        model = Industry
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model"""
    industry_detail = IndustrySerializer(source='industry_model', read_only=True)
    full_name = serializers.ReadOnlyField()
    location = serializers.ReadOnlyField()
    
    class Meta:
        model = Contact
        fields = [
            # Basic Info
            'id', 'first_name', 'last_name', 'full_name', 'title', 'seniority', 'departments',
            
            # Contact Info
            'email', 'email_status', 'primary_email_catch_all_status',
            'work_direct_phone', 'home_phone', 'mobile_phone', 'corporate_phone', 'other_phone',
            
            # Company Info
            'company', 'company_name_for_emails', 'industry', 'industry_model', 'industry_detail',
            'employees', 'stage',
            
            # Financial
            'annual_revenue', 'total_funding', 'latest_funding', 'latest_funding_amount', 'last_raised_at',
            
            # Location
            'city', 'state', 'country', 'location',
            'company_address', 'company_city', 'company_state', 'company_country', 'company_phone',
            
            # Social & Web
            'person_linkedin_url', 'company_linkedin_url', 'facebook_url', 'twitter_url', 'website',
            
            # Metadata
            'technologies', 'keywords', 'contact_id', 'account_id',
            
            # Timestamps
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ContactListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Contact
        fields = [
            'id', 'full_name', 'title', 'email', 'company', 
            'city', 'country', 'industry', 'employees',
            'created_at'
        ]

