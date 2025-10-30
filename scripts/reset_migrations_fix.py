"""
Fix migration inconsistency by updating the django_migrations table
This fixes the InconsistentMigrationHistory error
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection


def fix_migration_history():
    """Fix the migration history inconsistency"""
    with connection.cursor() as cursor:
        # Check if admin.0001_initial exists
        cursor.execute("""
            SELECT 1 FROM django_migrations 
            WHERE app = 'admin' AND name = '0001_initial';
        """)
        
        if cursor.fetchone() is None:
            print("Inserting missing admin.0001_initial migration...")
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                VALUES ('admin', '0001_initial', NOW())
                ON CONFLICT DO NOTHING;
            """)
            print("✓ Inserted admin.0001_initial")
        
        # Check if we need to reorder migrations
        cursor.execute("""
            SELECT id, app, name, applied 
            FROM django_migrations 
            WHERE app = 'admin' 
            ORDER BY id;
        """)
        
        rows = cursor.fetchall()
        print(f"\nFound {len(rows)} admin migrations")
        for row in rows:
            print(f"  {row[1]}.{row[2]} - {row[3]}")
        
        print("\n✓ Migration history should now be consistent")
        return True


if __name__ == '__main__':
    print("Fixing Django Migration Inconsistency")
    print("=" * 50)
    
    try:
        fix_migration_history()
        print("\n✓ Migration history fixed!")
        print("\nNow you can run: python manage.py migrate")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

