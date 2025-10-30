"""Update import_jobs table to use BigInteger for file_size"""
import sys
sys.path.insert(0, '.')

print("Step 1: Importing modules...")
from sqlalchemy import text
from config.database import engine

print("Step 2: Connecting to database...")

try:
    with engine.connect() as conn:
        print("Step 3: Starting transaction...")
        trans = conn.begin()
        
        try:
            # Check current column type
            print("Step 4: Checking current schema...")
            result = conn.execute(text("""
                SELECT data_type FROM information_schema.columns 
                WHERE table_name = 'import_jobs' AND column_name = 'file_size'
            """))
            current_type = result.fetchone()
            print(f"Current type: {current_type}")
            
            if current_type and current_type[0] == 'integer':
                # Update the column type
                print("Step 5: Updating column type to BIGINT...")
                conn.execute(text("ALTER TABLE import_jobs ALTER COLUMN file_size TYPE BIGINT"))
                trans.commit()
                print("✅ Schema updated successfully")
            else:
                trans.rollback()
                print(f"Column type is already {current_type}")
                
        except Exception as e:
            trans.rollback()
            print(f"Error in transaction: {e}")
            import traceback
            traceback.print_exc()
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

