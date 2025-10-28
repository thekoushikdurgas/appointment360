"""
CSV Service - Handle CSV import/export operations
"""
import pandas as pd
import io
from typing import Dict, List, Tuple
from datetime import datetime
import streamlit as st


class CSVService:
    @staticmethod
    def read_csv(file) -> pd.DataFrame:
        """Read CSV file"""
        try:
            df = pd.read_csv(file)
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
            return None
    
    @staticmethod
    def read_csv_file(file_path: str) -> pd.DataFrame:
        """Read CSV file from file path"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
            return None
    
    @staticmethod
    def validate_csv(df: pd.DataFrame, required_columns: List[str] = None) -> Tuple[bool, List[str]]:
        """Validate CSV structure"""
        errors = []
        
        if df is None or df.empty:
            errors.append("CSV file is empty")
            return False, errors
        
        if required_columns:
            missing = set(required_columns) - set(df.columns)
            if missing:
                errors.append(f"Missing required columns: {', '.join(missing)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def process_chunks(df: pd.DataFrame, chunk_size: int = 1000) -> List[pd.DataFrame]:
        """Process DataFrame in chunks"""
        chunks = []
        for i in range(0, len(df), chunk_size):
            chunks.append(df.iloc[i:i + chunk_size])
        return chunks
    
    @staticmethod
    def auto_detect_columns(df: pd.DataFrame) -> Dict[str, str]:
        """Auto-detect column types and map to contact fields"""
        mapping = {}
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Name fields
            if any(x in col_lower for x in ['first name', 'firstname', 'fname']):
                mapping[col] = 'first_name'
            elif any(x in col_lower for x in ['last name', 'lastname', 'lname']):
                mapping[col] = 'last_name'
            elif any(x in col_lower for x in ['name', 'full name', 'fullname']):
                mapping[col] = 'full_name'
            
            # Contact fields
            elif any(x in col_lower for x in ['email', 'e-mail']):
                mapping[col] = 'email'
            elif any(x in col_lower for x in ['phone', 'telephone', 'mobile']):
                mapping[col] = 'phone'
            
            # Company fields
            elif any(x in col_lower for x in ['company', 'organization', 'org']):
                mapping[col] = 'company'
            elif 'industry' in col_lower:
                mapping[col] = 'industry'
            elif any(x in col_lower for x in ['website', 'url', 'web']):
                mapping[col] = 'website'
            elif 'linkedin' in col_lower:
                mapping[col] = 'linkedin_url'
            
            # Job fields
            elif any(x in col_lower for x in ['title', 'position', 'job title', 'role']):
                mapping[col] = 'title'
            
            # Location fields
            elif 'city' in col_lower:
                mapping[col] = 'city'
            elif 'state' in col_lower:
                mapping[col] = 'state'
            elif 'country' in col_lower:
                mapping[col] = 'country'
            elif 'location' in col_lower:
                mapping[col] = 'location'
            
            # Other fields
            elif 'employees' in col_lower:
                mapping[col] = 'employees'
            elif 'revenue' in col_lower:
                mapping[col] = 'revenue'
        
        return mapping
    
    @staticmethod
    def preview_csv(df: pd.DataFrame, rows: int = 10) -> pd.DataFrame:
        """Show preview of CSV"""
        return df.head(rows)
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame) -> bytes:
        """Export DataFrame to CSV bytes"""
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue()
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame) -> bytes:
        """Export DataFrame to Excel bytes"""
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return buffer.getvalue()
