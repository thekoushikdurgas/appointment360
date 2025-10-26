#!/usr/bin/env python
"""
Setup script for Appointment360 Django Migration
"""

import os
import sys
import subprocess


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        print(e.stderr)
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("Appointment360 Django Migration - Setup")
    print("=" * 60)
    
    # Check if we're in the correct directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this from the project root.")
        sys.exit(1)
    
    # Step 1: Install dependencies
    print("\n📦 Step 1: Installing dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Step 2: Make migrations
    print("\n🗄️ Step 2: Creating database migrations...")
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    # Step 3: Apply migrations
    print("\n🗄️ Step 3: Applying migrations...")
    if not run_command("python manage.py migrate", "Applying migrations"):
        print("❌ Failed to apply migrations")
        sys.exit(1)
    
    # Step 4: Collect static files (optional)
    print("\n📁 Step 4: Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Success message
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the server: python manage.py runserver")
    print("3. Access at: http://localhost:8000/admin/login/")
    print("\nFor more information, see:")
    print("- README_DJANGO.md")
    print("- docs/QUICK_START.md")
    print("\nHappy coding! 🚀")


if __name__ == "__main__":
    main()
