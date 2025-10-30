#!/bin/bash
# Deployment script for Appointment360

echo "🚀 Starting deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create logs directory
mkdir -p logs

# Setup Celery (if needed)
echo "⚙️  Setting up Celery workers..."

echo "✅ Deployment complete!"
echo "📝 Next steps:"
echo "1. Update .env file with production credentials"
echo "2. Run: python manage.py runserver"
echo "3. Run Celery: celery -A appointment360 worker --loglevel=info"

