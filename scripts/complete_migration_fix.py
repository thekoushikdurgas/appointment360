"""
Complete migration fix - fake all remaining migrations since tables exist
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

print("=" * 60)
print("Complete Migration Fix")
print("=" * 60)

# List of apps with tables that already exist
apps_to_fake = ['contacts', 'imports', 'exports']

for app in apps_to_fake:
    print(f"\nFaking {app} migrations...")
    try:
        call_command('migrate', app, '--fake', verbosity=2, interactive=False)
        print(f"✅ Successfully faked {app} migrations")
    except Exception as e:
        print(f"❌ Error with {app}: {e}")
        # Try to fake individual migrations
        import glob
        migration_files = glob.glob(f'apps/{app}/migrations/*_initial.py')
        if migration_files:
            migration_name = migration_files[0].split('/')[-1].replace('.py', '')
            try:
                call_command('migrate', app, migration_name, '--fake', verbosity=2, interactive=False)
                print(f"✅ Faked {app}.{migration_name}")
            except:
                pass

print("\n" + "=" * 60)
print("Migration process complete!")
print("=" * 60)

# Check final status
print("\nFinal migration status:")
try:
    call_command('showmigrations')
except Exception as e:
    print(f"Error: {e}")

