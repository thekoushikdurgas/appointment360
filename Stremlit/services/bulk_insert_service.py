"""
Bulk Insert Service - Optimized database insertion for large imports
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Optional
from models.contact import Contact
from pyspark.sql import DataFrame
import json
import pandas as pd
from datetime import datetime


class BulkInsertService:
    """Handle bulk inserts to database with optimized performance"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def bulk_insert_from_dataframe(self, df: DataFrame, user_id: int = 1) -> Dict:
        """
        Insert records from Spark DataFrame to database
        Returns dict with success count, error count, and errors
        """
        results = {
            'success_count': 0,
            'error_count': 0,
            'errors': []
        }
        
        try:
            # Convert to Pandas for easier iteration
            pdf = df.toPandas()
            
            # Prepare batch data
            batch_size = 1000
            total_batches = (len(pdf) + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, len(pdf))
                batch = pdf.iloc[start_idx:end_idx]
                
                # Convert to dict list for bulk insert
                records = []
                for _, row in batch.iterrows():
                    record = self._row_to_dict(row, user_id)
                    if record:
                        records.append(record)
                
                # Bulk insert this batch
                try:
                    self.db.bulk_insert_mappings(Contact, records)
                    self.db.commit()
                    results['success_count'] += len(records)
                except Exception as e:
                    self.db.rollback()
                    results['error_count'] += len(records)
                    results['errors'].append({
                        'batch': batch_idx + 1,
                        'error': str(e),
                        'row_count': len(records)
                    })
        
        except Exception as e:
            results['errors'].append({
                'type': 'general',
                'error': str(e)
            })
        
        return results
    
    def _row_to_dict(self, row, user_id: int) -> Optional[Dict]:
        """Convert DataFrame row to contact dictionary"""
        try:
            record = {
                'full_name': str(row.get('full_name', '')).strip() or self._build_full_name(row),
                'first_name': str(row.get('first_name', '')).strip(),
                'last_name': str(row.get('last_name', '')).strip(),
                'email': str(row.get('email', '')).strip().lower(),
                'phone': str(row.get('phone', '')).strip(),
                'title': str(row.get('title', '')).strip(),
                'company': str(row.get('company', '')).strip(),
                'industry': str(row.get('industry', '')).strip(),
                'company_size': str(row.get('company_size', '')).strip(),
                'company_address': str(row.get('company_address', '')).strip(),
                'website': str(row.get('website', '')).strip(),
                'city': str(row.get('city', '')).strip(),
                'state': str(row.get('state', '')).strip(),
                'country': str(row.get('country', '')).strip(),
                'postal_code': str(row.get('postal_code', '')).strip(),
                'company_city': str(row.get('company_city', '')).strip(),
                'company_state': str(row.get('company_state', '')).strip(),
                'company_country': str(row.get('company_country', '')).strip(),
                'company_phone': str(row.get('company_phone', '')).strip(),
                'linkedin': str(row.get('linkedin', '')).strip(),
                'person_linkedin_url': str(row.get('person_linkedin_url', '')).strip(),
                'company_linkedin_url': str(row.get('company_linkedin_url', '')).strip(),
                'facebook_url': str(row.get('facebook_url', '')).strip(),
                'twitter_url': str(row.get('twitter_url', '')).strip(),
                'notes': str(row.get('notes', '')).strip(),
                'tags': str(row.get('tags', '')).strip(),
                'user_id': user_id,
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # Handle numeric fields
            try:
                record['employees_count'] = int(row.get('employees_count', 0)) if pd.notna(row.get('employees_count')) else None
            except:
                record['employees_count'] = None
            
            try:
                record['annual_revenue'] = int(row.get('annual_revenue', 0)) if pd.notna(row.get('annual_revenue')) else None
            except:
                record['annual_revenue'] = None
            
            try:
                record['total_funding'] = int(row.get('total_funding', 0)) if pd.notna(row.get('total_funding')) else None
            except:
                record['total_funding'] = None
            
            # Extended fields
            record['seniority'] = str(row.get('seniority', '')).strip()
            record['departments'] = str(row.get('departments', '')).strip()
            record['keywords'] = str(row.get('keywords', '')).strip()
            record['technologies'] = str(row.get('technologies', '')).strip()
            record['email_status'] = str(row.get('email_status', '')).strip()
            record['stage'] = str(row.get('stage', '')).strip()
            
            # Validate required fields
            if not record.get('email') or not record.get('first_name'):
                return None
            
            return record
            
        except Exception as e:
            print(f"Error converting row to dict: {str(e)}")
            return None
    
    def _build_full_name(self, row) -> str:
        """Build full name from first and last name"""
        first = str(row.get('first_name', '')).strip()
        last = str(row.get('last_name', '')).strip()
        return f"{first} {last}".strip()
    
    def get_existing_emails_batch(self, emails: List[str]) -> List[str]:
        """Get list of emails that already exist in database (for deduplication)"""
        try:
            from sqlalchemy import create_engine, text
            from config.database import engine
            
            # Query database for existing emails
            with engine.connect() as conn:
                query = text(f"SELECT email FROM contacts WHERE email IN :emails")
                result = conn.execute(query, {'emails': tuple(emails)})
                existing = [row[0] for row in result]
                return existing
        except Exception as e:
            print(f"Error checking existing emails: {str(e)}")
            return []
    
    def check_duplicates_in_batch(self, df: DataFrame) -> DataFrame:
        """Check which emails already exist in database"""
        try:
            # Get unique emails from DataFrame
            emails = df.select("email").distinct().collect()
            email_list = [row.email for row in emails]
            
            # Check which exist in database
            existing_emails = self.get_existing_emails_batch(email_list)
            existing_set = set(existing_emails)
            
            # Mark duplicates
            from pyspark.sql.functions import when, col, lit
            df_with_flag = df.withColumn(
                "is_duplicate",
                when(col("email").isin(list(existing_set)), lit(True))
                .otherwise(lit(False))
            )
            
            return df_with_flag
        except Exception as e:
            print(f"Error checking duplicates: {str(e)}")
            return df

