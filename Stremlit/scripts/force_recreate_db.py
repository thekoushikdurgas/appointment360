"""
Force Recreate Database - Drop and recreate with new schema
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from config.database import engine, Base
from models.contact import Contact
from models.import_job import ImportJob
from models.export_log import ExportLog
from models.user import User

print("🔄 Recreating database with new schema...")

try:
    # Drop all tables
    print("🗑️  Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped")
    
    # Create all tables with new schema
    print("📋 Creating new tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ New tables created")
    
    print("\n✅ Database recreated successfully!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

