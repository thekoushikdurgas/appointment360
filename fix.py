import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("Fixing migration history...")

with connection.cursor() as cursor:
    # Delete problematic admin migration
    cursor.execute("DELETE FROM django_migrations WHERE app = 'admin' AND name = '0001_initial';")
    affected = cursor.rowcount
    print(f"Deleted {affected} admin migration record(s)")
    
    connection.commit()

print("Done! Now run: python manage.py migrate")


