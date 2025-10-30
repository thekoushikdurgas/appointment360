"""
Check current migration state in database
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection


def check_migration_state():
    """Check current migration state"""
    print("=" * 60)
    print("Checking Django Migration State")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Check if django_migrations table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'django_migrations'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("❌ django_migrations table does not exist")
            print("This is a fresh database - no migrations have been run")
            return
        
        print("✓ django_migrations table exists\n")
        
        # Get all admin migrations
        cursor.execute("""
            SELECT app, name, applied 
            FROM django_migrations 
            WHERE app IN ('admin', 'accounts', 'auth', 'contenttypes')
            ORDER BY app, name;
        """)
        
        migrations = cursor.fetchall()
        
        if not migrations:
            print("No migrations found in database")
            return
        
        print("Current Migration State:")
        print("-" * 60)
        
        current_app = None
        for app, name, applied in migrations:
            if current_app != app:
                current_app = app
                print(f"\n📦 {app.upper()}")
            status = "✅ Applied" if applied else "❌ Not Applied"
            print(f"  {name} - {status}")
        
        # Check for the specific problematic migration
        cursor.execute("""
            SELECT 1 FROM django_migrations 
            WHERE app = 'accounts' AND name = '0001_initial';
        """)
        accounts_initial = cursor.fetchone() is not None
        
        cursor.execute("""
            SELECT 1 FROM django_migrations 
            WHERE app = 'admin' AND name = '0001_initial';
        """)
        admin_initial = cursor.fetchone() is not None
        
        print("\n" + "=" * 60)
        print("Migration Dependency Check:")
        print("-" * 60)
        print(f"accounts.0001_initial: {'✅ Applied' if accounts_initial else '❌ Not Applied'}")
        print(f"admin.0001_initial: {'✅ Applied' if admin_initial else '❌ Not Applied'}")
        
        if admin_initial and not accounts_initial:
            print("\n⚠️ PROBLEM DETECTED:")
            print("admin.0001_initial is applied but accounts.0001_initial is not!")
            print("This causes the InconsistentMigrationHistory error.")
            print("\nRECOMMENDED FIX:")
            print("1. Fake the accounts.0001_initial migration")
            print("2. Then run regular migrations")
        elif accounts_initial:
            print("\n✓ Migration dependency is correct")
        
        # Check if users table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            );
        """)
        users_table_exists = cursor.fetchone()[0]
        print(f"\nusers table exists: {'✅ Yes' if users_table_exists else '❌ No'}")
        
        if users_table_exists and not accounts_initial:
            print("\n💡 Tables exist but migration not recorded!")
            print("Solution: Fake the accounts.0001_initial migration")


if __name__ == '__main__':
    try:
        check_migration_state()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

