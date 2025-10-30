import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def main():
    print("\n" + "=" * 80)
    print("Django Migration History Fix")
    print("=" * 80)
    
    try:
        with connection.cursor() as cursor:
            # Step 1: Show current state
            print("\n[Step 1] Current migration history:")
            cursor.execute("""
                SELECT app, name, applied 
                FROM django_migrations 
                WHERE app IN ('admin', 'accounts', 'auth', 'contenttypes', 'sessions')
                ORDER BY applied;
            """)
            
            rows = cursor.fetchall()
            if rows:
                print("-" * 80)
                for app, name, applied in rows:
                    print(f"{app:20} {name:30} {applied}")
                print("-" * 80)
            
            # Step 2: Find the problematic migration
            print("\n[Step 2] Searching for problematic migrations...")
            cursor.execute("""
                SELECT app, name, applied 
                FROM django_migrations 
                WHERE app = 'admin' AND name = '0001_initial';
            """)
            admin_migration = cursor.fetchone()
            
            cursor.execute("""
                SELECT app, name, applied 
                FROM django_migrations 
                WHERE app = 'accounts' AND name = '0001_initial';
            """)
            accounts_migration = cursor.fetchone()
            
            if admin_migration and accounts_migration:
                print(f"  Found admin.0001_initial applied at:  {admin_migration[2]}")
                print(f"  Found accounts.0001_initial applied at: {accounts_migration[2]}")
                
                if admin_migration[2] < accounts_migration[2]:
                    print("\n  ✗ PROBLEM: Admin applied before accounts!")
                    
                    # Step 3: Fix by deleting admin migration
                    print("\n[Step 3] Fixing by removing admin.0001_initial from history...")
                    cursor.execute("""
                        DELETE FROM django_migrations 
                        WHERE app = 'admin' AND name = '0001_initial';
                    """)
                    print("  ✓ Deleted admin.0001_initial")
                    print("  ✓ Remaining accounts.0001_initial will be re-applied on migrate")
                    
                else:
                    print("\n  ✓ Order is correct")
            elif admin_migration and not accounts_migration:
                print("\n  Found admin.0001_initial but NOT accounts.0001_initial")
                print("\n[Step 3] Removing admin.0001_initial...")
                cursor.execute("""
                    DELETE FROM django_migrations 
                    WHERE app = 'admin' AND name = '0001_initial';
                """)
                print("  ✓ Deleted admin.0001_initial")
            else:
                print("\n  Migrations not found in expected state")
            
            # Commit the transaction
            connection.commit()
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 80)
    print("✓ Fix applied! Now run: python manage.py migrate")
    print("=" * 80)
    return 0

if __name__ == '__main__':
    sys.exit(main())


