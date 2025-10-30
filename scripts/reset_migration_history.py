import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("=" * 80)
print("Fixing Django Migration History")
print("=" * 80)

try:
    with connection.cursor() as cursor:
        # Show all migrations
        print("\nCurrent migrations in database:")
        cursor.execute("SELECT app, name, applied FROM django_migrations ORDER BY applied LIMIT 50")
        rows = cursor.fetchall()
        
        if rows:
            print("-" * 80)
            for app, name, applied in rows:
                print(f"{app:15} {name:30} {applied}")
            print("-" * 80)
        
        # Delete admin.0001_initial if it exists
        cursor.execute("DELETE FROM django_migrations WHERE app = 'admin' AND name = '0001_initial';")
        deleted = cursor.rowcount
        print(f"\n✓ Deleted {deleted} admin.0001_initial record(s)")
        
        # Commit the changes
        connection.commit()
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("Now run: python manage.py migrate")
print("=" * 80)


