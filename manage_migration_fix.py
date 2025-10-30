#!/usr/bin/env python
"""Run this script to fix the migration history issue."""
import subprocess
import sys

def run_migrate_fix():
    """Run the migration fix commands."""
    print("=" * 80)
    print("Fixing Django Migration History")
    print("=" * 80)
    
    # Step 1: Try to fake the migrations in the right order
    print("\nStep 1: Attempting to fake admin migration dependencies...")
    subprocess.run([sys.executable, "manage.py", "migrate", "--fake", "admin", "0001"], check=False)
    
    # Step 2: Show what's in the database
    print("\nStep 2: Checking migration status...")
    subprocess.run([sys.executable, "manage.py", "showmigrations"], check=False)
    
    print("\n" + "=" * 80)
    print("If issues persist, try:")
    print("  1. python manage.py migrate --fake admin zero")
    print("  2. python manage.py migrate")
    print("=" * 80)

if __name__ == "__main__":
    run_migrate_fix()


