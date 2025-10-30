# Test Suite Documentation

## Overview

This directory contains comprehensive pytest test cases for all flows, pages, and main components of the Appointment360 application.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── pytest.ini              # Pytest configuration
├── unit/                    # Unit tests by app
│   ├── accounts/           # Authentication tests
│   ├── contacts/           # Contact management tests
│   ├── core/               # Dashboard and core features
│   ├── imports/            # CSV import functionality
│   ├── exports/            # Export functionality
│   ├── analytics/          # Analytics and charts
│   ├── jobs/               # Job scraper
│   ├── settings/           # User settings
│   └── services/           # Service layer tests
├── integration/            # End-to-end flow tests
└── fixtures/               # Test data files
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific App Tests
```bash
pytest tests/unit/accounts/
pytest tests/unit/contacts/
```

### Run with Coverage
```bash
pytest --cov=apps --cov=services --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/unit/contacts/test_views.py
```

### Run Specific Test
```bash
pytest tests/unit/contacts/test_views.py::TestContactListView::test_contact_list_view_get
```

### Run with Markers
```bash
pytest -m "unit"                    # Run only unit tests
pytest -m "integration"            # Run only integration tests
pytest -m "not slow"                # Skip slow tests
```

## Test Coverage

### Current Coverage Goals
- **Models**: 95%+ coverage
- **Views**: 90%+ coverage
- **Services**: 95%+ coverage
- **Forms**: 100% coverage
- **API Endpoints**: 95%+ coverage

### View Coverage Report
```bash
pytest --cov=apps --cov=services --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Categories

### Unit Tests
- Model validation and methods
- View rendering and logic
- Form validation
- Service methods
- Utility functions

### Integration Tests
- Complete authentication flows
- Contact CRUD workflows
- Import/export workflows
- Analytics dashboard flow

## Fixtures

Common fixtures available in `conftest.py`:
- `user`: Test user
- `authenticated_client`: Authenticated Django test client
- `contact`: Sample contact instance
- `multiple_contacts`: Multiple test contacts
- `csv_file`: Temporary CSV file for testing
- `import_job`: Sample import job
- `export_log`: Sample export log
- `mock_supabase`: Mocked Supabase client
- `mock_celery`: Mocked Celery tasks
- `mock_playwright`: Mocked Playwright browser

## Writing New Tests

### Example Test Structure
```python
import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestMyView:
    """Test my view"""
    
    def test_view_loads(self, authenticated_client):
        """Test view loads correctly"""
        response = authenticated_client.get(reverse('myapp:view'))
        assert response.status_code == 200
```

## Mocking External Services

- **Supabase**: Use `mock_supabase` fixture
- **Celery**: Use `mock_celery` fixture
- **Playwright**: Use `mock_playwright` fixture

## Notes

- All database operations use test database (auto-created by pytest-django)
- External API calls are mocked
- File operations use temporary files
- Tests are isolated and can run in parallel

