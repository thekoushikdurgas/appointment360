"""
Database initialization script
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import init_db, get_db
from sqlalchemy.orm import Session

def main():
    print("🚀 Initializing database...")
    
    try:
        # Initialize tables
        init_db()
        print("✅ Database tables created")
        print("✅ Database initialization complete!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
