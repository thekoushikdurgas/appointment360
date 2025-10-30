"""
Configuration settings for Contact Management System
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://woqnlgszvkqxaqabtqfv.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndvcW5sZ3N6dmtxeGFxYWJ0cWZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzMTM4ODYsImV4cCI6MjA3Njg4OTg4Nn0.DpePQML323-gdbbPxidrq-up8PXeBdXlG_8AtcIMW0o')

# Application Configuration
PAGE_TITLE = "Appointment360 - Contact Management System"
PAGE_ICON = "📅"

# Database Configuration (PostgreSQL Only)
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'aws-1-ap-southeast-1.pooler.supabase.com')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 6543))
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres.evsjreawstqtkcsbwfjt')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'F5jhYj-X3Wx!nf7')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres.evsjreawstqtkcsbwfjt:F5jhYj-X3Wx!nf7@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres')

# Session Configuration
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Upload Configuration
MAX_UPLOAD_SIZE = os.getenv('MAX_UPLOAD_SIZE', '10485760000')  # Default 10GB for large imports
ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.xls']

# Pagination
CONTACTS_PER_PAGE = 50

# Data Folder Configuration
DATA_FOLDER_PATH = os.getenv('DATA_FOLDER_PATH', str(BASE_DIR / 'data'))

# Export Configuration
DEFAULT_DOWNLOAD_LIMIT = 100  # Default number of allowed downloads per day

# PySpark Configuration
SPARK_DRIVER_MEMORY = os.getenv('SPARK_DRIVER_MEMORY', '4g')
SPARK_EXECUTOR_MEMORY = os.getenv('SPARK_EXECUTOR_MEMORY', '4g')
IMPORT_BATCH_SIZE = int(os.getenv('IMPORT_BATCH_SIZE', '10000'))
MAX_IMPORT_WORKERS = int(os.getenv('MAX_IMPORT_WORKERS', '4'))

