"""
Direct migration fix by manipulating the database migration table
This is a surgical fix for the specific inconsistency issue
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=" * 60)
print("Direct Migration Fix")
print("=" * 60)

with connection.cursor() as cursor:
    # Check if accounts.0001_initial is already recorded
    cursor.execute("""
        SELECT 1 FROM django_migrations 
        WHERE app = 'accounts' AND name = '0001_initial';
    """)
    
    exists = cursor.fetchone()
    
    if exists:
        print("✓ accounts.0001_initial migration is already recorded")
    else:
        print("Adding accounts.0001_initial to migration history...")
        
        # Insert the missing migration record
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('accounts', '0001_initial', CURRENT_TIMESTAMP);
        """)
        
        print("✅ Added accounts.0001_initial to migration history")
    
    # Also check and add 0002 if needed
    cursor.execute("""
        SELECT 1 FROM django_migrations 
        WHERE app = 'accounts' AND name = '0002_add_profile_fields';
    """)
    
    exists_0002 = cursor.fetchone()
    
    if not exists_0002:
        print("\nNote: accounts.0002_add_profile_fields migration will be applied next")

print("\n" + "=" * 60)
print("Migration history updated successfully!")
print("=" * 60)

# Now try to run migrations
print("\nRunning migrations...")
from django.core.management import call_command

try:
    call_command('migrate', verbosity=2)
    print("\n✅ All migrations applied successfully!")
except Exception as e:
    print(f"\n❌ Error during migration: {e}")
    print("\nYou may need to run: python manage.py migrate --fake")

