# Quick Start Guide - Appointment360 Django

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8+ installed
- pip installed
- (Optional) Redis for Celery
- (Optional) PostgreSQL for production

---

## Step 1: Setup Environment

```bash
# Navigate to Django directory
cd Django

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure Environment Variables

Create a `.env` file in the Django directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (using SQLite by default)
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3

# AWS S3 (leave empty for now if not using)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1

# Celery (using local Redis)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Razorpay (leave empty for now if not using)
RAZORPAY_KEY=
RAZORPAY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
```

---

## Step 3: Run Migrations

```bash
# Create database and tables
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
# Follow prompts to create admin user
```

---

## Step 4: Start the Server

```bash
# Start Django development server
python manage.py runserver

# Server will run at http://localhost:8000
```

---

## Step 5: (Optional) Start Celery Worker

In a new terminal:

```bash
# Make sure Redis is running
# Then start Celery worker
celery -A appointment360 worker --loglevel=info
```

---

## Access the Application

### Admin Panel
- URL: http://localhost:8000/admin/
- Login with superuser credentials

### API Documentation
- URL: http://localhost:8000/api/api/contacts/

### API Endpoints
- Authentication: http://localhost:8000/api/auth/
- Contacts: http://localhost:8000/api/api/contacts/
- Dashboard: http://localhost:8000/api/api/dashboard/stats/

---

## Testing the API

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123"}'
```

**Get Contacts:**
```bash
curl http://localhost:8000/api/api/contacts/
```

### Using Python

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'email': 'admin@example.com',
    'password': 'password123'
})

# Get session cookie
session = requests.Session()
session.cookies.update(response.cookies)

# Get contacts
response = session.get('http://localhost:8000/api/api/contacts/')
print(response.json())
```

---

## Running with Docker

### Quick Start with Docker Compose

```bash
# Start all services (database, Redis, web, Celery)
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Common Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Create new migrations
python manage.py makemigrations

# Run Django shell
python manage.py shell

# Check project
python manage.py check
```

---

## Troubleshooting

### Issue: Module not found errors
**Solution:** Make sure you've activated virtual environment and installed requirements

### Issue: Database locked errors
**Solution:** SQLite doesn't support concurrent writes. Switch to PostgreSQL in production

### Issue: Celery worker not starting
**Solution:** Make sure Redis is running: `redis-server`

### Issue: AWS S3 errors
**Solution:** Make sure AWS credentials are correct in .env file

---

## Next Steps

1. ✅ Server is running
2. ⏭️ Create contacts via admin panel or API
3. ⏭️ Test CSV upload functionality
4. ⏭️ Test export to Excel
5. ⏭️ Configure production environment

---

## Development vs Production

### Development
- Uses SQLite database
- Debug mode enabled
- Console email backend
- Local file storage

### Production
- Use PostgreSQL/MySQL
- Debug mode disabled
- SMTP email backend
- AWS S3 storage
- Use Docker deployment

---

## Support

- Check logs in `logs/django.log`
- Review `README.md` for detailed documentation
- See `IMPLEMENTATION_STATUS.md` for feature status
- Review `api_documentation.md` for API details

