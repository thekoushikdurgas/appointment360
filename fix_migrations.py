"""
Fix migration inconsistency by faking the accounts.0001_initial migration
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

print("=" * 60)
print("Fixing Migration Inconsistency")
print("=" * 60)

# Step 1: Fake the accounts.0001_initial migration since tables already exist
print("\nStep 1: Faking accounts.0001_initial migration...")
try:
    call_command('migrate', 'accounts', '0001_initial', '--fake', verbosity=2)
    print("✅ Successfully faked accounts.0001_initial")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Step 2: Now run all migrations normally
print("\nStep 2: Running all remaining migrations...")
try:
    call_command('migrate', verbosity=2)
    print("✅ All migrations applied successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("Migration Fix Complete!")
print("=" * 60)
