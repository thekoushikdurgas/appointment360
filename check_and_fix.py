import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=" * 80)
print("Checking migration history...")
print("=" * 80)

with connection.cursor() as cursor:
    # Show problematic migrations
    cursor.execute("""
        SELECT app, name, applied 
        FROM django_migrations 
        WHERE app IN ('admin', 'accounts', 'auth', 'contenttypes', 'sessions')
        ORDER BY app, name;
    """)
    
    print("\nMigrations in database:")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:20} {row[1]:30} {row[2]}")
    print("-" * 80)
    
    # Check for the specific error
    cursor.execute("""
        SELECT * FROM django_migrations 
        WHERE app = 'admin' AND name = '0001_initial';
    """)
    admin_row = cursor.fetchone()
    
    cursor.execute("""
        SELECT * FROM django_migrations 
        WHERE app = 'accounts' AND name = '0001_initial';
    """)
    accounts_row = cursor.fetchone()
    
    if admin_row and accounts_row:
        admin_time = admin_row[2]
        accounts_time = accounts_row[2]
        
        print(f"\nAdmin migration time:  {admin_time}")
        print(f"Accounts migration time: {accounts_time}")
        
        if admin_time < accounts_time:
            print("\nERROR: Admin migration applied BEFORE accounts migration!")
            print("This is the source of the inconsistency.")
            print("\nFixing by deleting admin.0001_initial from history...")
            
            cursor.execute("""
                DELETE FROM django_migrations 
                WHERE app = 'admin' AND name = '0001_initial';
            """)
            print("✓ Deleted admin.0001_initial from migration history")
            print("\nNow run: python manage.py migrate")
        else:
            print("\n✓ Migration order is correct")
    elif admin_row and not accounts_row:
        print("\nAccounts migration not found. Admin migration exists.")
        print("This suggests accounts migration needs to be run.")
        
    elif not admin_row and accounts_row:
        print("\nAdmin migration not found. This is OK.")
        
print("\n" + "=" * 80)


