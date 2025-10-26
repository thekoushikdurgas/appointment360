# Appointment360 - Django Migration

Contact Management System migrated from Laravel 8 to Django 5.x

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)

### Installation

```bash
# Clone or navigate to project directory
cd appointment360.com

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Follow prompts to create username, email, and password

# Run development server
python manage.py runserver
```

### Access the Application

- **Web Interface:** http://localhost:8000/admin/login/
- **Admin Panel:** http://localhost:8000/admin/
- **Dashboard:** http://localhost:8000/dashboard/
- **Contacts:** http://localhost:8000/admin/contacts/
- **Users:** http://localhost:8000/admin/users/

## 📁 Project Structure

```
appointment360/
├── apps/
│   ├── accounts/         # Authentication
│   ├── contacts/         # Contact management
│   ├── dashboard/        # Dashboard
│   ├── users/            # User management
│   ├── uploads/          # File uploads
│   └── payments/         # Payment integration
├── templates/
│   ├── layouts/          # Base templates
│   ├── admin/            # Admin pages
│   └── dashboard/        # Dashboard pages
├── static/               # Static files
├── media/                # User-uploaded files
└── docs/                 # Documentation
```

## 🎯 Features

### ✅ Implemented
- **Authentication System**
  - Login with remember me
  - Logout
  - Password reset via email
  - Profile management
  
- **User Management**
  - Create, read, update, delete users
  - Role-based access control (admin, user, manager)
  - Download limit management
  - Status toggle
  - Column visibility permissions
  
- **Contact Management**
  - View contact list
  - Create/edit contacts
  - Import page (structure ready)
  - Advanced filtering API
  - Export to Excel
  
- **Dashboard**
  - Statistics display
  - Quick action buttons
  - User metrics
  - Contact count
  
- **Layout System**
  - Responsive design
  - Sidebar navigation
  - User dropdown menu
  - Footer

### ⏳ In Progress
- CSV import for large files
- Payment integration (Razorpay)
- Additional pages
- Static assets migration

## 🔐 Default Credentials

After creating superuser:
- Email: [your email]
- Password: [your password]
- Role: admin (default)

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/password-reset/` - Request password reset
- `GET /api/auth/profile/` - Get profile

### Contacts
- `GET /api/contacts/` - List contacts (with filters)
- `POST /api/contacts/` - Create contact
- `GET /api/contacts/<id>/` - Get contact details
- `PUT /api/contacts/<id>/` - Update contact
- `DELETE /api/contacts/<id>/` - Delete contact
- `POST /api/contacts/export/` - Export contacts

### Users
- `GET /admin/users/` - List users (admin only)
- `GET /admin/users/create/` - Create user form
- `POST /admin/users/create/` - Create user
- `GET /admin/users/<id>/edit/` - Edit user form
- `POST /admin/users/<id>/edit/` - Update user

## 🗄️ Database Models

### AdminUser
Custom user model with:
- Role-based access (admin, user, manager)
- Download limits
- IP tracking
- Password reset tokens

### Contact
Contact information with 48+ fields:
- Personal info (name, title, email, phones)
- Company info (company, industry, employees)
- Location (city, state, country)
- Financial data (revenue, funding)
- Social media links
- Technologies and keywords

### Industry
Industry categorization for contacts

## 🛠️ Development

### Running Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Migrations
```bash
python manage.py makemigrations apps.appname
```

### Accessing Django Admin
```bash
python manage.py createsuperuser
# Then visit http://localhost:8000/admin/
```

### Static Files
```bash
python manage.py collectstatic
```

## 📝 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### Settings
Key settings in `appointment360/settings.py`:
- Custom user model: `AUTH_USER_MODEL = 'accounts.AdminUser'`
- Login URL: `LOGIN_URL = '/admin/login/'`
- Static files: Configured for both development and production

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test apps.accounts
python manage.py test apps.contacts
```

## 🚢 Production Deployment

### Settings for Production
1. Set `DEBUG=False`
2. Configure `ALLOWED_HOSTS`
3. Generate new `SECRET_KEY`
4. Setup PostgreSQL database
5. Configure static file serving
6. Setup SSL certificates
7. Configure email backend

### Deployment Commands
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn appointment360.wsgi:application

# Or with uWSGI
uwsgi --ini uwsgi.ini
```

## 📚 Documentation

- `docs/MIGRATION_STATUS.md` - Detailed migration status
- `docs/MIGRATION_COMPLETE.md` - Completion summary
- `docs/IMPLEMENTATION_SUMMARY.md` - Implementation details
- `docs/QUICK_START.md` - Quick start guide
- `docs/STATIC_FILES_SETUP.md` - Static files configuration

## 🐛 Troubleshooting

### Issue: Database locked
```bash
# Delete db.sqlite3 and rerun migrations
rm db.sqlite3
python manage.py migrate
```

### Issue: Static files not loading
```bash
# Run collectstatic
python manage.py collectstatic
# Clear browser cache
```

### Issue: Module import errors
```bash
# Ensure you're in the project directory
# Check INSTALLED_APPS in settings.py
```

## 📞 Support

For issues or questions:
1. Check documentation in `/docs/`
2. Review migration status
3. Check Django logs in `/logs/django.log`

## 📄 License

MIT License - Free Software

## 🙏 Acknowledgments

- Migrated from Laravel 8 to Django 5.x
- Based on SB Admin 2 theme
- Using Bootstrap 4, jQuery, DataTables

---

**Status:** 75% Complete - Core features + CSV Import functional  
**Last Updated:** January 27, 2025

## Recent Updates

### ✅ CSV Import System (90% Complete)
- Chunked multipart upload to S3
- Background processing with Celery
- Real-time progress tracking
- Upload cancellation support
- Complete field mapping (48+ fields)
- Comprehensive error handling

### ✅ Testing Infrastructure Started
- Test suite created for accounts app
- Test suite created for uploads app
- Test patterns established

