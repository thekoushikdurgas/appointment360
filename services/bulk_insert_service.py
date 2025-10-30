"""
Bulk Insert Service - Optimized database inserts for large CSV imports
Migrated from Stremlit/services/bulk_insert_service.py
"""
from typing import List, Dict, Any, Optional
import pandas as pd
from apps.contacts.models import Contact
from services.type_converter import TypeConverter
from services.import_error_tracker import ImportErrorTracker


class BulkInsertService:
    """Handle bulk inserts of contacts with error tracking"""
    
    def __init__(self, db_session=None):
        """
        Initialize bulk insert service
        
        Args:
            db_session: Django doesn't need explicit session like SQLAlchemy
        """
        self.error_tracker = ImportErrorTracker()
    
    def bulk_insert_from_dataframe(self, df: pd.DataFrame, user_id: str, 
                                   column_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Bulk insert contacts from DataFrame
        
        Args:
            df: Pandas DataFrame with contact data
            user_id: User ID for the contacts
            column_mapping: Mapping of CSV columns to database fields
            
        Returns:
            Dictionary with success_count, error_count, and duplicate_count
        """
        success_count = 0
        error_count = 0
        duplicate_count = 0
        
        for idx, row in df.iterrows():
            try:
                # Build contact data from mapping
                contact_data = {}
                
                for csv_col, db_field in column_mapping.items():
                    if csv_col in row.index:
                        value = row[csv_col]
                        if pd.notna(value) and str(value).strip() != '':
                            # Use type converter to properly handle numeric fields
                            converted_value = TypeConverter.convert_value(db_field, value)
                            contact_data[db_field] = converted_value
                
                # Set user_id
                contact_data['user_id'] = str(user_id)
                
                # Clean and merge names
                contact_data = TypeConverter.clean_and_merge_names(contact_data)
                
                # Skip if email already exists
                email = contact_data.get('email')
                if email:
                    existing = Contact.objects.filter(email=email).first()
                    if existing:
                        duplicate_count += 1
                        self.error_tracker.add_duplicate_error(idx + 1, email)
                        continue
                
                # Validate required fields
                if not email:
                    error_count += 1
                    self.error_tracker.add_validation_error(
                        idx + 1, 'email', contact_data.get('email'), 'Email is required'
                    )
                    continue
                
                # Create contact
                contact = Contact(**contact_data)
                contact.save()
                success_count += 1
                
            except Exception as e:
                error_count += 1
                self.error_tracker.add_error(
                    idx + 1,
                    'unknown',
                    f"Error: {str(e)}",
                    str(row.to_dict())
                )
                continue
        
        return {
            'success_count': success_count,
            'error_count': error_count,
            'duplicate_count': duplicate_count,
            'total_processed': len(df)
        }
    
    def bulk_insert_chunked(self, df: pd.DataFrame, user_id: str, 
                           column_mapping: Dict[str, str], 
                           chunk_size: int = 100) -> Dict[str, Any]:
        """
        Bulk insert contacts in chunks with progress tracking
        
        Args:
            df: Pandas DataFrame with contact data
            user_id: User ID for the contacts
            column_mapping: Mapping of CSV columns to database fields
            chunk_size: Number of records to process before committing
            
        Returns:
            Dictionary with success_count, error_count, duplicate_count
        """
        total_success = 0
        total_error = 0
        total_duplicate = 0
        
        # Process in chunks
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i + chunk_size]
            chunk_results = self.bulk_insert_from_dataframe(chunk, user_id, column_mapping)
            
            total_success += chunk_results['success_count']
            total_error += chunk_results['error_count']
            total_duplicate += chunk_results['duplicate_count']
        
        return {
            'success_count': total_success,
            'error_count': total_error,
            'duplicate_count': total_duplicate,
            'total_processed': len(df)
        }
    
    def get_errors(self) -> List:
        """Get all errors from tracker"""
        return self.error_tracker.get_errors()
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get error summary"""
        return self.error_tracker.get_error_summary()
    
    def get_error_tracker(self) -> ImportErrorTracker:
        """Get the error tracker instance"""
        return self.error_tracker
    
    def clear_errors(self):
        """Clear error tracker"""
        self.error_tracker.clear()

