"""
CSV Column Mapper - Map CSV columns to database fields
Migrated from Stremlit/services/csv_column_mapper.py
"""
from typing import Dict, List
import pandas as pd


class CSVColumnMapper:
    """Map CSV columns to Django model fields"""
    
    def __init__(self):
        self.field_mappings = {
            # Personal Information
            'first_name': ['first name', 'firstname', 'fname', 'first'],
            'last_name': ['last name', 'lastname', 'lname', 'last'],
            'full_name': ['name', 'full name', 'fullname', 'full'],
            'email': ['email', 'e-mail', 'email address', 'e mail'],
            'phone': ['phone', 'telephone', 'tel', 'mobile', 'cell', 'work_direct_phone', 
                     'home_phone', 'mobile_phone', 'corporate_phone', 'other_phone'],
            'title': ['title', 'position', 'job title', 'role', 'designation'],
            
            # Company Information
            'company': ['company', 'organization', 'org', 'company name', 'company_name_for_emails'],
            'industry': ['industry', 'sector', 'vertical'],
            'company_size': ['company_size', 'employees', 'employee count', 'size'],
            'company_address': ['company_address', 'company address', 'corporate address'],
            'website': ['website', 'url', 'web', 'site', 'company_website'],
            
            # Extended Company Fields
            'employees_count': ['employees', 'employee count', 'size', 'company_size'],
            'annual_revenue': ['annual_revenue', 'annual revenue', 'revenue', 'sales', 'turnover'],
            'total_funding': ['total_funding', 'total funding'],
            'latest_funding_amount': ['latest_funding_amount', 'latest funding amount', 'funding amount'],
            
            # Location Fields
            'city': ['city', 'town'],
            'state': ['state', 'province', 'region'],
            'country': ['country', 'nation'],
            'company_city': ['company_city', 'company city', 'corporate city'],
            'company_state': ['company_state', 'company state', 'corporate state'],
            'company_country': ['company_country', 'company country', 'corporate country'],
            'company_phone': ['company_phone', 'company phone', 'corporate_phone', 'corporate phone'],
            'postal_code': ['postal_code', 'postal code', 'zip', 'zip code'],
            
            # Extended Person Fields
            'seniority': ['seniority', 'level', 'seniority level'],
            'departments': ['departments', 'department'],
            'keywords': ['keywords', 'tags', 'skills', 'key words'],
            'technologies': ['technologies', 'tech', 'stack', 'technology stack'],
            'email_status': ['email_status', 'email status', 'email verification'],
            'stage': ['stage', 'lead stage', 'lead_status'],
            
            # Social Media
            'person_linkedin_url': ['person_linkedin_url', 'person linkedin', 'linkedin url', 
                                   'linkedin_profile', 'personal linkedin'],
            'company_linkedin_url': ['company_linkedin_url', 'company linkedin', 
                                    'company_linkedin', 'company linkedin url'],
            'linkedin': ['linkedin', 'linkedin profile', 'linkedin url'],
            'facebook_url': ['facebook_url', 'facebook url', 'facebook'],
            'twitter_url': ['twitter_url', 'twitter url', 'twitter', 'twitter_handle'],
            'facebook': ['facebook', 'fb'],
            'twitter': ['twitter', 'twitter handle'],
            
            # Other Fields
            'notes': ['notes', 'note', 'description', 'comments'],
            'tags': ['tags', 'tag', 'categories'],
            'status': ['status', 'lead status', 'contact status'],
        }
    
    def auto_map_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Auto-map CSV columns to database fields with fuzzy matching"""
        mapping = {}
        
        for col in df.columns:
            col_lower = col.lower().strip()
            col_cleaned = col_lower.replace('_', ' ').replace('-', ' ')
            
            # Try exact match first
            if col_lower in self.field_mappings:
                mapping[col] = col_lower
                continue
            
            # Try to find matching field with keyword matching
            best_match = None
            best_score = 0
            
            for field, keywords in self.field_mappings.items():
                for keyword in keywords:
                    # Exact match gets highest score
                    if keyword == col_lower or keyword == col_cleaned:
                        if col not in mapping:
                            mapping[col] = field
                            best_match = field
                            best_score = 100
                            break
                    # Check if keyword is contained in column name
                    elif keyword in col_lower or keyword in col_cleaned:
                        score = len(keyword) / len(col_lower)
                        if score > best_score:
                            best_match = field
                            best_score = score
            
            if best_match and col not in mapping:
                mapping[col] = best_match
        
        return mapping
    
    def validate_mapping(self, mapping: Dict[str, str]) -> List[str]:
        """Validate column mapping for conflicts"""
        errors = []
        
        # Check for duplicate target fields
        target_fields = list(mapping.values())
        duplicates = [field for field in target_fields if target_fields.count(field) > 1]
        
        if duplicates:
            errors.append(f"Duplicate mappings found for: {', '.join(set(duplicates))}")
        
        return errors
    
    def apply_mapping(self, df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """Apply column mapping to DataFrame"""
        # Rename columns
        df_mapped = df.rename(columns=mapping)
        
        # Keep only mapped columns (remove unmapped)
        mapped_columns = [col for col in df_mapped.columns if col in mapping.values()]
        df_mapped = df_mapped[mapped_columns]
        
        return df_mapped

