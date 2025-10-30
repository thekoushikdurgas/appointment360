"""
Final migration fix - simplifies by using Django's built-in --fake option
with proper database manipulation
"""
import os
import sys
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=" * 60)
print("Final Migration Fix")
print("=" * 60)

# Check current state
with connection.cursor() as cursor:
    cursor.execute("SELECT app, name, applied FROM django_migrations WHERE app = 'accounts';")
    results = cursor.fetchall()
    
    if results:
        print("\nCurrent accounts migrations:")
        for app, name, applied in results:
            print(f"  {name} - applied={applied}")
    else:
        print("\nNo accounts migrations found")
    
    # Check if we need to add 0001_initial
    cursor.execute("""
        SELECT 1 FROM django_migrations 
        WHERE app = 'accounts' AND name = '0001_initial';
    """)
    
    if not cursor.fetchone():
        print("\nAdding accounts.0001_initial to migration history...")
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('accounts', '0001_initial', CURRENT_TIMESTAMP);
        """)
        print("✅ Added accounts.0001_initial")

print("\nNow checking if we can apply the new migration...")
from django.core.management import call_command

# Show what needs to be migrated
print("\nChecking migration status...")
try:
    call_command('showmigrations')
except Exception as e:
    print(f"\nError showing migrations: {e}")
    print("\nThis is expected if there are dependency issues.")

# Try to fake initial for accounts
print("\nAttempting to fake accounts migrations...")
try:
    call_command('migrate', 'accounts', '0001_initial', '--fake', verbosity=2, interactive=False)
    print("✅ Successfully faked accounts.0001_initial")
except Exception as e:
    print(f"Could not fake 0001: {e}")

# Now run migrate normally
print("\nRunning all migrations...")
try:
    call_command('migrate', verbosity=2, interactive=False)
    print("\n✅ Successfully applied all migrations!")
except Exception as e:
    print(f"\nMigration error: {e}")
    
    # If we got the inconsistency error, try one more fix
    if "InconsistentMigrationHistory" in str(e):
        print("\n\nAttempting alternative fix...")
        # Delete admin migrations and rerun
        with connection.cursor() as cursor:
            print("Temporarily removing problematic admin migrations...")
            cursor.execute("""
                DELETE FROM django_migrations 
                WHERE app = 'admin' AND name IN ('0002_logentry_remove_auto_add', '0003_logentry_add_action_flag_choices');
            """)
            print("Removed admin.0002 and admin.0003 from history")
            
            # Now try migrate again
            try:
                call_command('migrate', verbosity=2, interactive=False)
                print("\n✅ Successfully applied all migrations!")
            except Exception as e2:
                print(f"\nStill error: {e2}")
                print("\nManual intervention may be required.")

print("\n" + "=" * 60)

