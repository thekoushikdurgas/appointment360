# Contact Manager - Comprehensive Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [API Documentation](#api-documentation)
7. [Frontend Components](#frontend-components)
8. [Real-time Updates](#real-time-updates)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Contributing](#contributing)

## Project Overview

Contact Manager is a comprehensive Django-based web application for managing contacts, imports, exports, and analytics. It provides a modern, responsive interface with real-time updates and advanced features.

### Key Technologies
- **Backend**: Django 4.2+, Python 3.9+
- **Frontend**: Bootstrap 5, Alpine.js, Plotly.js
- **Database**: PostgreSQL (production), SQLite (development)
- **Real-time**: WebSockets (Django Channels), Server-Sent Events
- **Background Tasks**: Celery with Redis
- **Authentication**: Django's built-in authentication system

## Architecture

### Project Structure
```
appoinment360.com/
├── apps/
│   ├── accounts/          # User authentication and profiles
│   ├── analytics/         # Analytics dashboard and charts
│   ├── contacts/          # Contact management
│   ├── core/             # Core functionality and progress tracking
│   ├── exports/          # Export functionality and history
│   ├── imports/          # Import functionality and progress tracking
│   ├── jobs/             # Job scraping functionality
│   └── settings/         # User settings and feature toggles
├── config/               # Django project configuration
├── static/               # Static files (CSS, JS, images)
├── templates/            # Django templates
└── services/             # Business logic services
```

### Database Models

#### Core Models
- **TaskCategory**: Categories for organizing development tasks
- **TaskTracker**: Individual tasks with completion tracking
- **UserSettings**: User preferences and configuration
- **FeatureToggle**: Global feature toggles
- **UserFeatureToggle**: User-specific feature overrides
- **SystemSettings**: System-wide configuration

#### Contact Models
- **Contact**: Main contact information
- **ContactImport**: Import job tracking
- **ContactExport**: Export job tracking

## Features

### 1. Contact Management
- **CRUD Operations**: Create, read, update, delete contacts
- **Bulk Operations**: Select multiple contacts for bulk actions
- **Search & Filter**: Advanced filtering by industry, country, status
- **Data Validation**: Comprehensive form validation
- **Import/Export**: CSV, Excel, JSON support

### 2. Import System
- **Progress Tracking**: Real-time progress updates
- **Batch Processing**: Large file handling with chunked processing
- **Error Handling**: Detailed error reporting and logging
- **Column Mapping**: Automatic and manual column mapping
- **Duplicate Detection**: Smart duplicate handling

### 3. Export System
- **Multiple Formats**: CSV, Excel, JSON export
- **Filtered Exports**: Export based on search criteria
- **Bulk Exports**: Export selected contacts
- **History Tracking**: Complete export history
- **Download Management**: File management and cleanup

### 4. Analytics Dashboard
- **Interactive Charts**: Plotly.js-powered visualizations
- **Industry Distribution**: Pie charts for industry analysis
- **Country Distribution**: Geographic data visualization
- **Growth Trends**: Time-series analysis
- **Top Companies**: Bar charts for company analysis
- **Status Distribution**: Contact status breakdown

### 5. Progress Tracker
- **Task Management**: Organize development tasks by category
- **Completion Tracking**: Visual progress indicators
- **Priority Management**: Task prioritization system
- **Real-time Updates**: Live progress updates
- **Sidebar Integration**: Compact progress display

### 6. Settings Management
- **User Preferences**: Theme, language, layout preferences
- **Feature Toggles**: Enable/disable features per user
- **Notification Settings**: Email and push notification preferences
- **Privacy Controls**: Data retention and sharing settings
- **Import/Export Settings**: Default formats and options

### 7. Real-time Updates
- **WebSocket Integration**: Django Channels for real-time updates
- **Server-Sent Events**: SSE for lightweight real-time communication
- **AJAX Polling**: Intelligent polling with exponential backoff
- **Progress Updates**: Live import/export progress
- **Notification System**: Real-time notifications

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Node.js 16+ (for frontend assets)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd appoinment360.com
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup database**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Collect static files**
```bash
python manage.py collectstatic
```

6. **Run development server**
```bash
python manage.py runserver
```

### Docker Setup

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/contact_manager

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
DEBUG=False

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Django Settings
Key settings in `config/settings.py`:
- Database configuration
- Static files settings
- Media files settings
- Celery configuration
- WebSocket configuration

## API Documentation

### Core API Endpoints

#### Progress Tracker
- `GET /api/categories/` - Get task categories
- `GET /api/tasks/` - Get all tasks
- `POST /api/tasks/<id>/toggle/` - Toggle task completion
- `GET /api/progress-stats/` - Get progress statistics

#### Settings API
- `GET /api/get-settings/` - Get user settings
- `POST /api/update/` - Update user settings
- `POST /api/toggle-feature/<id>/` - Toggle feature

#### Import API
- `GET /api/job/<id>/status/` - Get import job status
- `POST /api/job/<id>/cancel/` - Cancel import job
- `GET /api/recent-jobs/` - Get recent import jobs

#### Export API
- `GET /api/status/<id>/` - Get export status
- `GET /api/download/<id>/` - Download export file
- `POST /api/cancel/<id>/` - Cancel export
- `POST /api/bulk-delete/` - Bulk delete exports

#### Analytics API
- `GET /api/stats/` - Get analytics statistics
- `GET /api/chart-data/<type>/` - Get chart data

### Server-Sent Events
- `GET /sse/updates/` - Real-time updates stream
- `POST /sse/send-notification/` - Send notification
- `GET /sse/status/` - SSE connection status

## Frontend Components

### Alpine.js Components

#### Toast Notification
```javascript
// Usage
Alpine.data('toastNotification', toastNotification);
```

#### Loading Spinner
```javascript
// Usage
Alpine.data('loadingSpinner', loadingSpinner);
```

#### Modal Component
```javascript
// Usage
Alpine.data('modalComponent', modalComponent);
```

#### Form Validation
```javascript
// Usage
Alpine.data('formValidation', formValidation);
```

#### Data Table
```javascript
// Usage
Alpine.data('dataTable', dataTable);
```

#### File Upload
```javascript
// Usage
Alpine.data('fileUpload', fileUpload);
```

#### Progress Bar
```javascript
// Usage
Alpine.data('progressBar', progressBar);
```

### Utility Functions

#### Date Utils
```javascript
ContactManagerUtils.DateUtils.formatDate(date, format);
ContactManagerUtils.DateUtils.formatRelativeTime(date);
ContactManagerUtils.DateUtils.formatDuration(milliseconds);
```

#### File Utils
```javascript
ContactManagerUtils.FileUtils.formatFileSize(bytes);
ContactManagerUtils.FileUtils.getFileExtension(filename);
ContactManagerUtils.FileUtils.downloadFile(url, filename);
```

#### String Utils
```javascript
ContactManagerUtils.StringUtils.truncate(str, length);
ContactManagerUtils.StringUtils.capitalize(str);
ContactManagerUtils.StringUtils.slugify(str);
```

#### Validation Utils
```javascript
ContactManagerUtils.ValidationUtils.isValidEmail(email);
ContactManagerUtils.ValidationUtils.isValidPhone(phone);
ContactManagerUtils.ValidationUtils.isValidURL(url);
```

## Real-time Updates

### WebSocket Integration
- **Django Channels**: WebSocket support for real-time updates
- **Consumer**: Handles WebSocket connections and message routing
- **Routing**: URL routing for WebSocket connections

### Server-Sent Events
- **SSE Manager**: JavaScript class for handling SSE connections
- **Auto-reconnect**: Automatic reconnection with exponential backoff
- **Event Handling**: Structured event handling system

### AJAX Polling
- **Polling Manager**: Intelligent polling with backoff strategies
- **Mixin Support**: Alpine.js mixin for easy integration
- **Error Handling**: Comprehensive error handling and retry logic

## Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.core
python manage.py test apps.settings

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Structure
- **Unit Tests**: Model and utility function tests
- **Integration Tests**: API endpoint tests
- **Frontend Tests**: JavaScript component tests
- **End-to-End Tests**: Complete workflow tests

### Test Coverage
- Models: 95%+ coverage
- Views: 90%+ coverage
- API Endpoints: 95%+ coverage
- JavaScript Components: 80%+ coverage

## Deployment

### Production Setup

1. **Environment Configuration**
```bash
export DEBUG=False
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:password@host:port/db
export REDIS_URL=redis://host:port/0
```

2. **Static Files**
```bash
python manage.py collectstatic --noinput
```

3. **Database Migration**
```bash
python manage.py migrate
```

4. **Celery Worker**
```bash
celery -A config worker -l info
```

5. **WebSocket Server**
```bash
daphne -b 0.0.0.0 -p 8001 config.asgi:application
```

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /ws/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    location /static/ {
        alias /path/to/static/files/;
    }
    
    location /media/ {
        alias /path/to/media/files/;
    }
}
```

## Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
```bash
git checkout -b feature/new-feature
```
3. **Make changes and commit**
```bash
git commit -m "Add new feature"
```
4. **Write tests**
5. **Run tests**
```bash
python manage.py test
```
6. **Create pull request**

### Code Style
- **Python**: Follow PEP 8
- **JavaScript**: Use ESLint configuration
- **CSS**: Follow BEM methodology
- **Django**: Follow Django best practices

### Commit Messages
Use conventional commit format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- **Issues**: GitHub Issues
- **Documentation**: Project Wiki
- **Email**: support@example.com

## Changelog

### Version 1.0.0
- Initial release
- Contact management system
- Import/export functionality
- Analytics dashboard
- Progress tracking
- Settings management
- Real-time updates
- Comprehensive testing