#!/usr/bin/env python
"""
Fix inconsistent Django migration history in the database.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def check_migration_history():
    """Check the current migration history in the database."""
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
            print("django_migrations table does not exist. Creating it...")
            call_command('migrate', '--fake', verbosity=0)
            return
        
        # Get all migrations for the apps mentioned in the error
        cursor.execute("""
            SELECT app, name, applied 
            FROM django_migrations 
            WHERE app IN ('admin', 'auth', 'accounts', 'contenttypes', 'sessions')
            ORDER BY applied;
        """)
        
        migrations = cursor.fetchall()
        
        print("\nCurrent migration history for problematic apps:")
        print("-" * 80)
        for app, name, applied in migrations:
            print(f"{app:15} {name:30} {applied}")
        print("-" * 80)
        
        # Check for the specific problematic migration
        cursor.execute("""
            SELECT * FROM django_migrations 
            WHERE app = 'admin' AND name = '0001_initial';
        """)
        
        admin_initial = cursor.fetchone()
        if admin_initial:
            print(f"\nFound admin.0001_initial at: {admin_initial}")
        
        # Check for accounts.0001_initial
        cursor.execute("""
            SELECT * FROM django_migrations 
            WHERE app = 'accounts' AND name = '0001_initial';
        """)
        
        accounts_initial = cursor.fetchone()
        if accounts_initial:
            print(f"Found accounts.0001_initial at: {accounts_initial}")
        else:
            print("accounts.0001_initial NOT found in database")

def fix_migration_history():
    """Fix the inconsistent migration history."""
    print("\nAttempting to fix migration history...")
    
    # Option 1: Fake the missing dependencies
    print("\nStep 1: Faking missing migrations to establish dependencies...")
    
    # The issue is that admin.0001_initial depends on accounts
    # but it was applied before accounts in the database
    
    with connection.cursor() as cursor:
        # Check if accounts.0001_initial exists
        cursor.execute("""
            SELECT * FROM django_migrations 
            WHERE app = 'accounts' AND name = '0001_initial';
        """)
        
        if not cursor.fetchone():
            print("Adding missing accounts.0001_initial to migration history...")
            # Insert the missing migration with a timestamp earlier than admin
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                VALUES ('accounts', '0001_initial', CURRENT_TIMESTAMP - INTERVAL '1 minute');
            """)
            print("✓ Added accounts.0001_initial")
        
        # Delete admin.0001_initial and reapply it
        cursor.execute("""
            DELETE FROM django_migrations 
            WHERE app = 'admin' AND name = '0001_initial';
        """)
        print("✓ Removed admin.0001_initial from history")
    
    print("\nStep 2: Running migrations to rebuild history...")
    try:
        call_command('migrate', '--fake-initial', verbosity=1)
        print("\n✓ Migrations completed successfully!")
    except Exception as e:
        print(f"\n✗ Error during migration: {e}")
        print("\nAttempting alternative fix...")
        
        # Alternative: Reset the database migration history
        print("Clearing problematic migrations from history...")
        
        with connection.cursor() as cursor:
            # Delete all problematic migrations
            cursor.execute("""
                DELETE FROM django_migrations 
                WHERE app IN ('admin', 'accounts')
                AND name LIKE '%0001_initial%';
            """)
        
        print("\nRerunning migrations from scratch...")
        call_command('migrate', '--fake-initial', verbosity=1)

if __name__ == '__main__':
    print("=" * 80)
    print("Django Migration History Fixer")
    print("=" * 80)
    
    check_migration_history()
    fix_migration_history()
    
    print("\n" + "=" * 80)
    print("Done! Try running: python manage.py migrate")
    print("=" * 80)


