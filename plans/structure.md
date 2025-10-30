# Django Contact Management System - Project Structure

## Directory Structure

```
django_contact_manager/
│
├── apps/                              # Django applications
│   ├── __init__.py
│   │
│   ├── core/                          # Dashboard & Home
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                  # (Empty - core logic only)
│   │   ├── views.py                   # Dashboard view with charts
│   │   ├── urls.py                    # URL routing
│   │   └── admin.py
│   │
│   ├── accounts/                      # Authentication
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                  # User model with Supabase fields
│   │   ├── views.py                   # Login, logout, signup
│   │   ├── urls.py                    # Auth URLs
│   │   ├── forms.py                   # (If needed)
│   │   ├── auth_backends.py          # Supabase auth backend
│   │   ├── middleware.py             # Session management
│   │   └── admin.py
│   │
│   ├── contacts/                     # Contact Management
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                  # Contact model (40+ fields)
│   │   ├── views.py                   # List, Create, Update, Delete, Export
│   │   ├── forms.py                   # ContactForm
│   │   ├── urls.py                    # Contact URLs
│   │   ├── admin.py                   # Django admin for Contact
│   │   └── filters.py                 # (Optional - for advanced filtering)
│   │
│   ├── imports/                       # CSV Import System
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                  # ImportJob model
│   │   ├── views.py                   # Upload, preview, start import
│   │   ├── urls.py                    # Import URLs
│   │   ├── forms.py                   # (If needed)
│   │   ├── tasks.py                   # Celery tasks
│   │   ├── consumers.py               # WebSocket consumers
│   │   ├── routing.py                 # WebSocket routing
│   │   └── admin.py                   # Django admin for ImportJob
│   │
│   ├── analytics/                     # Analytics & Reporting
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                  # (Optional - for analytics models)
│   │   ├── views.py                   # Analytics dashboard, data quality
│   │   ├── urls.py                    # Analytics URLs
│   │   └── admin.py
│   │
│   └── exports/                       # Export Tracking
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py                  # ExportLog, ExportLimit models
│       ├── views.py                   # Export history view
│       ├── urls.py                    # Export URLs
│       └── admin.py                    # Admin for exports
│
├── config/                            # Django project configuration
│   ├── __init__.py                    # Celery app initialization
│   ├── settings.py                     # Django settings
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py                        # WSGI config for Gunicorn
│   ├── asgi.py                        # ASGI config for Daphne/Channels
│   └── celery.py                      # Celery configuration
│
├── services/                          # Business Logic Layer
│   ├── __init__.py
│   ├── contact_service.py             # Contact CRUD operations
│   ├── csv_column_mapper.py           # CSV column auto-mapping
│   └── spark_import_service.py       # PySpark integration (placeholder)
│
├── templates/                         # HTML Templates
│   ├── base.html                      # Base template with sidebar
│   │
│   ├── accounts/                      # Authentication pages
│   │   ├── login.html
│   │   └── signup.html
│   │
│   ├── core/                          # Dashboard
│   │   └── dashboard.html
│   │
│   ├── contacts/                      # Contact pages
│   │   ├── list.html                  # Contact list with search/filter
│   │   ├── form.html                  # Create/Edit form
│   │   └── delete_confirm.html        # Delete confirmation
│   │
│   ├── imports/                       # Import pages
│   │   ├── upload.html                # File upload
│   │   ├── preview.html                # CSV preview
│   │   └── progress.html              # Progress tracking
│   │
│   └── components/                    # Reusable components
│       ├── sidebar.html               # Navigation sidebar
│       ├── hero_section.html          # Page headers
│       ├── metric_card.html           # Metric display cards
│       └── progress_tracker.html      # Progress widget
│
├── static/                            # Static Files
│   ├── css/
│   │   └── custom.css                 # Custom styling
│   └── js/
│       └── main.js                    # Main JavaScript
│
├── media/                             # User uploaded files (created at runtime)
│   └── temp/                          # Temporary files
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .env                               # Actual environment variables
├── .gitignore                         # Git ignore rules
├── .dockerignore                      # Docker ignore rules
│
├── Dockerfile                         # Docker container definition
├── docker-compose.yml                 # Multi-container setup
├── gunicorn.conf.py                   # Gunicorn configuration
│
└── Documentation/
    ├── README.md                      # Main readme
    ├── SETUP_GUIDE.md                 # Setup instructions
    ├── DEPLOYMENT.md                  # Deployment guide
    ├── PROGRESS.md                    # Progress tracker
    ├── IMPLEMENTATION_STATUS.md       # Status report
    ├── COMPLETION_SUMMARY.md          # Completion summary
    ├── FINAL_STATUS.md                # Final status
    ├── SUCCESS_SUMMARY.md             # Success summary
    └── MIGRATION_COMPLETE.md          # Migration summary
```

## File Count by Type

- **Python Files**: ~50 files
- **Templates**: ~15 files
- **Static Files**: 2 files
- **Config Files**: 9 files
- **Documentation**: 8 files
- **Total**: ~90 files

## Key Components

### Models (5)
- `User` - Custom user with Supabase integration
- `Contact` - Contact with 40+ fields
- `ImportJob` - Background job tracking
- `ExportLog` - Export history
- `ExportLimit` - Daily export limits

### Views (6 apps)
- `core` - Dashboard
- `accounts` - Authentication
- `contacts` - CRUD operations
- `imports` - CSV import
- `analytics` - Analytics & quality
- `exports` - Export tracking

### Services (3)
- `ContactService` - Contact operations
- `CSVColumnMapper` - Column mapping
- `SparkImportService` - Large file processing

### Templates (15+)
- Base layout
- Login/Signup
- Dashboard
- Contact pages (list, form, delete)
- Import pages (upload, preview, progress)
- Reusable components

### Configuration (7)
- Django settings
- URL routing
- ASGI/WSGI
- Celery
- Database
- Static files
- Media files

## Database Schema

```
users
├── id
├── email
├── supabase_user_id
├── supabase_email
├── role
└── timestamps

contacts
├── id
├── Personal (first_name, last_name, full_name, email, phone, title)
├── Company (company, industry, company_size, website)
├── Extended Company (employees_count, annual_revenue, funding)
├── Location (city, state, country, postal_code)
├── Company Location (company_city, company_state, company_country)
├── Social Media (linkedin, facebook, twitter)
├── Additional (notes, tags, status, is_active)
└── timestamps

import_jobs
├── id
├── user_id, filename, file_size
├── Progress (total_rows, processed_rows, success_count, error_count)
├── Status (status, started_at, completed_at)
└── timestamps

export_logs
├── id
├── user_id, export_type, export_format
├── record_count, file_size, filename
└── timestamps
```

## Technology Stack

- **Backend**: Django 5.0
- **Database**: PostgreSQL (Supabase)
- **Cache**: Redis
- **Task Queue**: Celery
- **WebSocket**: Channels
- **Frontend**: Bootstrap 5 + Tailwind CSS
- **Charts**: Plotly
- **Containerization**: Docker
- **Production Server**: Gunicorn
- **WebSocket Server**: Daphne
- **Authentication**: Supabase

