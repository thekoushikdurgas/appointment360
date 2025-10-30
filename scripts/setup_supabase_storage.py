"""
Setup script for creating Supabase Storage buckets
Run this script to create required storage buckets in Supabase
"""
import os
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from services.supabase_storage_service import SupabaseStorageService
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_buckets():
    """Create required storage buckets in Supabase"""
    storage_service = SupabaseStorageService()
    
    buckets = [
        {
            'name': 'user-uploads',
            'public': True,
            'description': 'User-uploaded files (profile pictures, documents)'
        },
        {
            'name': 'documents',
            'public': False,
            'description': 'Private documents'
        },
    ]
    
    logger.info("Checking and creating Supabase storage buckets...")
    
    for bucket_info in buckets:
        bucket_name = bucket_info['name']
        
        if storage_service.bucket_exists(bucket_name):
            logger.info(f"✓ Bucket '{bucket_name}' already exists")
        else:
            logger.info(f"Creating bucket '{bucket_name}'...")
            success = storage_service.create_bucket(bucket_name, public=bucket_info['public'])
            
            if success:
                logger.info(f"✓ Bucket '{bucket_name}' created successfully")
            else:
                logger.error(f"✗ Failed to create bucket '{bucket_name}'")
    
    logger.info("\nBucket setup complete!")
    logger.info("\nNext steps:")
    logger.info("1. Go to your Supabase dashboard")
    logger.info("2. Navigate to Storage section")
    logger.info("3. Configure bucket policies as needed")
    logger.info("4. Set up RLS (Row Level Security) policies if using private buckets")


if __name__ == '__main__':
    try:
        create_buckets()
    except Exception as e:
        logger.error(f"Error setting up storage: {e}")
        sys.exit(1)

