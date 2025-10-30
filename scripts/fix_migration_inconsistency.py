"""
Script to fix Django migration inconsistency
This script handles the InconsistentMigrationHistory error
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.core.management import call_command


def fix_migration_inconsistency():
    """Fix migration inconsistency by checking database state"""
    with connection.cursor() as cursor:
        # Check if migrations table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'django_migrations'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("Migration table doesn't exist. This is normal for a fresh database.")
            print("Running initial migrations...")
            try:
                call_command('migrate', '--run-syncdb', verbosity=2)
            except Exception as e:
                print(f"Error during migration: {e}")
                print("\nTrying to fake initial admin migrations...")
                try:
                    call_command('migrate', 'admin', '0001_initial', '--fake', verbosity=2)
                    call_command('migrate', verbosity=2)
                except Exception as e2:
                    print(f"Error: {e2}")
                    return False
            return True
        
        # Check current migrations
        print("Checking current migration state...")
        cursor.execute("""
            SELECT app, name, applied 
            FROM django_migrations 
            WHERE app = 'admin'
            ORDER BY name;
        """)
        
        migrations = cursor.fetchall()
        print(f"\nCurrent admin migrations in database: {len(migrations)}")
        for app, name, applied in migrations:
            print(f"  - {name}: Applied={applied}")
        
        # Try to fix by faking the initial admin migration if missing
        cursor.execute("""
            SELECT 1 FROM django_migrations 
            WHERE app = 'admin' AND name = '0001_initial';
        """)
        
        if cursor.fetchone() is None:
            print("\nMissing admin.0001_initial migration. Faking it...")
            try:
                call_command('migrate', 'admin', '0001_initial', '--fake', verbosity=2)
                print("Successfully faked admin.0001_initial")
            except Exception as e:
                print(f"Error faking migration: {e}")
                return False
        
        # Now try to run migrations normally
        print("\nRunning migrations...")
        try:
            call_command('migrate', verbosity=2)
            print("\n✓ Migrations completed successfully!")
            return True
        except Exception as e:
            print(f"\nError during migration: {e}")
            print("\nTrying alternative approach...")
            return False


def reset_django_migrations_table():
    """Reset the django_migrations table (use with caution!)"""
    print("\n⚠ WARNING: This will reset all migration history!")
    print("This should only be done if you're sure about your database state.")
    
    response = input("Do you want to reset the django_migrations table? (yes/no): ")
    if response.lower() != 'yes':
        print("Operation cancelled.")
        return False
    
    with connection.cursor() as cursor:
        # Delete all migration records
        cursor.execute("DELETE FROM django_migrations;")
        print("✓ Cleared django_migrations table")
    
    # Now fake all migrations
    print("Faking all migrations...")
    try:
        call_command('migrate', '--fake-initial', verbosity=2)
        print("✓ All migrations faked successfully!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == '__main__':
    print("Django Migration Fixer")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        success = reset_django_migrations_table()
    else:
        success = fix_migration_inconsistency()
    
    if not success:
        print("\n⚠ The migration issue persists.")
        print("You may need to:")
        print("1. Check your database state manually")
        print("2. Run: python fix_migration_inconsistency.py --reset (USE WITH CAUTION)")
        print("3. Contact your database administrator")
    
    sys.exit(0 if success else 1)


