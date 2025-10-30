"""
Supabase Storage Service
Handles file uploads, downloads, and management in Supabase Storage
"""
import os
import logging
from typing import Optional, List, Dict
from supabase import create_client, Client
from django.conf import settings

logger = logging.getLogger(__name__)

class SupabaseStorageService:
    """Service for managing files in Supabase Storage"""
    
    def __init__(self):
        """Initialize Supabase client"""
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            raise ValueError("Supabase credentials not configured in settings")
        
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )
        self.bucket = getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'user-uploads')
    
    def upload_file(
        self, 
        file, 
        path: str, 
        bucket: str = None,
        file_options: Dict = None
    ) -> Optional[str]:
        """
        Upload a file to Supabase Storage
        
        Args:
            file: Django UploadedFile or bytes/string
            path: Destination path in bucket (e.g., 'profiles/user123/avatar.jpg')
            bucket: Bucket name (defaults to configured bucket)
            file_options: Additional options for upload
        
        Returns:
            Public URL of uploaded file or None
        """
        try:
            bucket_name = bucket or self.bucket
            file_options = file_options or {}
            
            # Convert Django UploadedFile to bytes if needed
            if hasattr(file, 'read'):
                file_data = file.read()
            else:
                file_data = file
            
            # Upload file
            response = self.supabase.storage.from_(bucket_name).upload(
                path=path,
                file=file_data,
                file_options=file_options
            )
            
            logger.info(f"File uploaded successfully: {path} in bucket {bucket_name}")
            
            # Get public URL
            return self.get_public_url(path, bucket_name)
            
        except Exception as e:
            logger.error(f"Error uploading file {path}: {str(e)}")
            raise
    
    def get_public_url(self, path: str, bucket: str = None) -> str:
        """
        Get public URL for a file
        
        Args:
            path: File path in bucket
            bucket: Bucket name
        
        Returns:
            Public URL string
        """
        bucket_name = bucket or self.bucket
        response = self.supabase.storage.from_(bucket_name).get_public_url(path)
        return response
    
    def download_file(self, path: str, bucket: str = None) -> bytes:
        """
        Download a file from Supabase Storage
        
        Args:
            path: File path in bucket
            bucket: Bucket name
        
        Returns:
            File bytes
        """
        try:
            bucket_name = bucket or self.bucket
            response = self.supabase.storage.from_(bucket_name).download(path)
            return response
            
        except Exception as e:
            logger.error(f"Error downloading file {path}: {str(e)}")
            raise
    
    def delete_file(self, path: str, bucket: str = None) -> bool:
        """
        Delete a file from Supabase Storage
        
        Args:
            path: File path in bucket
            bucket: Bucket name
        
        Returns:
            True if successful, False otherwise
        """
        try:
            bucket_name = bucket or self.bucket
            self.supabase.storage.from_(bucket_name).remove([path])
            logger.info(f"File deleted successfully: {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file {path}: {str(e)}")
            return False
    
    def list_files(self, path: str = '', bucket: str = None) -> List[Dict]:
        """
        List files in a storage path
        
        Args:
            path: Folder path (e.g., 'profiles/')
            bucket: Bucket name
        
        Returns:
            List of file dictionaries
        """
        try:
            bucket_name = bucket or self.bucket
            response = self.supabase.storage.from_(bucket_name).list(path)
            return response
            
        except Exception as e:
            logger.error(f"Error listing files in {path}: {str(e)}")
            return []
    
    def create_bucket(self, bucket_name: str, public: bool = True) -> bool:
        """
        Create a storage bucket
        
        Args:
            bucket_name: Name of the bucket
            public: Whether bucket should be public
        
        Returns:
            True if successful
        """
        try:
            self.supabase.storage.create_bucket(
                bucket_name,
                options={"public": public}
            )
            logger.info(f"Bucket created: {bucket_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating bucket {bucket_name}: {str(e)}")
            return False
    
    def bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if a bucket exists
        
        Args:
            bucket_name: Name of the bucket
        
        Returns:
            True if bucket exists
        """
        try:
            buckets = self.supabase.storage.list_buckets()
            return any(b.name == bucket_name for b in buckets)
            
        except Exception as e:
            logger.error(f"Error checking bucket {bucket_name}: {str(e)}")
            return False
    
    def validate_file(self, file, allowed_types: List[str] = None, max_size: int = None) -> tuple:
        """
        Validate file before upload
        
        Args:
            file: File to validate
            allowed_types: List of allowed MIME types
            max_size: Maximum file size in bytes
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Default allowed types for profile pictures
        if allowed_types is None:
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        
        # Default max size: 5MB
        if max_size is None:
            max_size = 5 * 1024 * 1024
        
        # Check file type
        if hasattr(file, 'content_type') and file.content_type not in allowed_types:
            return False, f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
        
        # Check file size
        if hasattr(file, 'size') and file.size > max_size:
            return False, f"File size exceeds limit of {max_size / 1024 / 1024:.1f}MB"
        
        return True, None


# Singleton instance
_storage_service = None

def get_storage_service() -> SupabaseStorageService:
    """Get or create SupabaseStorageService instance"""
    global _storage_service
    if _storage_service is None:
        _storage_service = SupabaseStorageService()
    return _storage_service

