"""
Recreate Database Script - Drop and recreate all tables with new schema
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import engine, Base, drop_db, init_db


def main():
    print("=" * 60)
    print("⚠️  WARNING: This will DROP ALL TABLES and recreate them")
    print("=" * 60)
    
    response = input("\nAre you sure you want to proceed? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Operation cancelled")
        return
    
    try:
        print("\n🗑️  Dropping all existing tables...")
        drop_db()
        print("✅ Tables dropped")
        
        print("\n📋 Creating new tables with updated schema...")
        init_db()
        print("✅ New tables created")
        
        print("\n" + "=" * 60)
        print("✅ Database recreated successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

