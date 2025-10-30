"""
Recreate Tables with CASCADE - Force drop all tables and recreate
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from config.database import engine, Base
import time

print("=" * 60)
print("🔄 Recreating all tables with CASCADE")
print("=" * 60)

try:
    # Create connection and get raw connection
    with engine.connect() as conn:
        # Begin transaction
        trans = conn.begin()
        
        try:
            # Drop all tables with CASCADE
            print("\n🗑️  Dropping all tables...")
            
            # Get list of all tables
            result = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public' AND tablename NOT LIKE 'pg_%'
            """))
            tables = [row[0] for row in result]
            
            if tables:
                print(f"Found {len(tables)} tables to drop: {tables}")
                
                # Drop each table individually with CASCADE
                for table in tables:
                    print(f"  Dropping table: {table}")
                    conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                
                # Commit the transaction
                trans.commit()
                print(f"✅ Dropped {len(tables)} tables")
            else:
                print("ℹ️ No tables to drop")
                trans.commit()
            
        except Exception as e:
            trans.rollback()
            raise
    
    # Wait a moment for cleanup
    time.sleep(1)
    
    print("\n📋 Creating new tables...")
    # Create all tables with new schema
    Base.metadata.create_all(bind=engine)
    print("✅ New tables created")
    
    print("\n" + "=" * 60)
    print("✅ Database recreated successfully!")
    print("=" * 60)
    print("\nYou can now start the Streamlit application:")
    print("  streamlit run main.py")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    raise

