# Contact Management System - Developer Guide

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Setup & Installation](#setup--installation)
4. [Database Schema](#database-schema)
5. [Services](#services)
6. [Components](#components)
7. [Testing](#testing)
8. [Deployment](#deployment)

---

## Architecture Overview

### Technology Stack
- **Frontend**: Streamlit 1.28+
- **Backend**: Python 3.8+
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Supabase
- **Data Processing**: Pandas, PySpark
- **Export**: openpyxl
- **Charts**: Plotly

### Architecture Pattern
- **Service Layer Pattern** - Business logic in services
- **Repository Pattern** - Data access through services
- **MVC Pattern** - Pages, Services, Models separation

---

## Project Structure

```
contact-management-system/
├── config/                 # Configuration files
│   ├── database.py        # Database setup
│   └── settings.py        # Application settings
├── models/                # Database models
│   ├── contact.py        # Contact model
│   ├── user.py           # User model
│   └── export_log.py     # Export log model
├── services/              # Business logic services
│   ├── contact_service.py
│   ├── csv_service.py
│   ├── csv_column_mapper.py
│   ├── export_limit_service.py
│   ├── import_error_tracker.py
│   ├── auth_service_supabase.py
│   └── spark_service.py
├── pages/                 # Streamlit pages
│   ├── 1_🏠_Dashboard.py
│   ├── 2_📇_Contacts.py
│   ├── 3_📤_Import_Contacts.py
│   ├── 4_👥_User_Management.py
│   ├── 5_⚙️_Settings.py
│   ├── 6_📊_Analytics.py
│   ├── 7_🔍_Data_Quality.py
│   └── 8_📜_Export_History.py
├── components/            # Reusable components
│   ├── sidebar.py        # Sidebar component
│   └── progress_tracker.py
├── utils/                 # Utility functions
│   ├── validators.py     # Input validation
│   ├── helpers.py        # Helper functions
│   └── constants.py      # Constants
├── tests/                # Test files
│   ├── test_contact_service.py
│   ├── test_csv_service.py
│   └── test_validators.py
├── docs/                 # Documentation
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── README.md           # Project overview
```

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation Steps

1. **Clone Repository**
```bash
git clone <repository-url>
cd contact-management-system
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
Create `.env` file:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
```

5. **Initialize Database**
```bash
python scripts/init_db.py
```

6. **Run Application**
```bash
streamlit run main.py
```

### Dependencies

- **streamlit** - Web framework
- **supabase** - Authentication
- **pandas** - Data manipulation
- **sqlalchemy** - ORM
- **bcrypt** - Password hashing
- **openpyxl** - Excel export
- **plotly** - Charts
- **pyspark** - Large-scale processing
- **pytest** - Testing

---

## Database Schema

### Contact Model
```python
class Contact:
    id: Integer
    full_name: String
    first_name: String
    last_name: String
    title: String
    email: String (indexed)
    phone: String
    company: String (indexed)
    industry: String
    company_size: String
    company_address: Text
    website: String
    city: String
    state: String
    country: String (indexed)
    postal_code: String
    linkedin: String
    facebook: String
    twitter: String
    notes: Text
    tags: String
    status: String
    is_active: Boolean
    created_at: DateTime
    updated_at: DateTime
    user_id: Integer
```

### User Model
```python
class User:
    id: Integer
    email: String (indexed, unique)
    password_hash: String
    first_name: String
    last_name: String
    role: String (enum: admin, user, manager)
    is_active: Boolean
    created_at: DateTime
    updated_at: DateTime
```

### ExportLog Model
```python
class ExportLog:
    id: Integer
    user_id: Integer (indexed)
    export_type: String
    export_format: String
    record_count: Integer
    filename: String
    created_at: DateTime
```

---

## Services

### ContactService
**File**: `services/contact_service.py`

Handles all contact operations:
- `create_contact(contact_data)` - Create new contact
- `get_contact(contact_id)` - Get contact by ID
- `get_contact_by_email(email)` - Get contact by email
- `update_contact(contact_id, contact_data)` - Update contact
- `delete_contact(contact_id)` - Delete contact
- `search_contacts(query, limit)` - Search contacts
- `filter_contacts(filters, page, per_page)` - Filter with pagination
- `get_contact_stats()` - Get statistics

### CSVService
**File**: `services/csv_service.py`

Handles CSV operations:
- `read_csv(file)` - Read CSV file
- `validate_csv(df, required_columns)` - Validate CSV structure
- `process_chunks(df, chunk_size)` - Process in chunks
- `auto_detect_columns(df)` - Auto-detect column mappings
- `export_to_csv(df)` - Export to CSV bytes
- `export_to_excel(df)` - Export to Excel bytes

### SparkService
**File**: `services/spark_service.py`

Handles large-scale processing:
- `read_csv(file_path)` - Read CSV with Spark
- `process_large_import(file_path, schema)` - Process large imports
- `deduplicate_contacts(df, threshold)` - Find duplicates
- `analyze_data_quality(df)` - Quality analysis
- `aggregate_statistics(df)` - Calculate statistics

---

## Components

### Sidebar Component
**File**: `components/sidebar.py`

Navigation sidebar with:
- User info display
- Page navigation
- Logout button

### Progress Tracker
**File**: `components/progress_tracker.py`

Visual progress indicator for imports.

---

## Testing

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_contact_service.py

# Run with coverage
pytest tests/ --cov=services --cov=utils
```

### Test Structure
- **Unit Tests** - Test individual functions
- **Integration Tests** - Test service interactions
- **Performance Tests** - Test with large datasets

### Writing Tests
```python
def test_create_contact(test_db):
    service = ContactService(test_db)
    
    contact_data = {
        'first_name': 'John',
        'email': 'john@example.com',
        'user_id': 1
    }
    
    contact = service.create_contact(contact_data)
    
    assert contact is not None
    assert contact.email == 'john@example.com'
```

---

## Deployment

### Production Setup

1. **Environment Variables**
```env
SUPABASE_URL=production_url
SUPABASE_ANON_KEY=production_key
DEBUG=False
```

2. **Database Migration**
```bash
# For PostgreSQL
python scripts/migrate_to_postgres.py
```

3. **Static Files**
```bash
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t contact-management .
docker run -p 8501:8501 contact-management
```

---

## Code Style

### Python Style Guide
Follow PEP 8:
- Use 4 spaces for indentation
- Line length: 79 characters
- Use docstrings for functions/classes
- Use type hints where appropriate

### Naming Conventions
- **Variables**: snake_case
- **Classes**: PascalCase
- **Functions**: snake_case
- **Constants**: UPPER_SNAKE_CASE

### Example
```python
def create_contact(contact_data: Dict) -> Contact:
    """Create a new contact with validation.
    
    Args:
        contact_data: Dictionary containing contact information
        
    Returns:
        Created Contact object
        
    Raises:
        ValueError: If email format is invalid
    """
    # Validation
    if not validate_email(contact_data.get('email')):
        raise ValueError("Invalid email format")
    
    # Create contact
    contact = Contact(**contact_data)
    return contact
```

---

## Performance Optimization

### Database
- Use indexes on frequently queried fields
- Implement pagination for large datasets
- Use batch operations when possible

### Caching
- Cache frequently accessed data
- Use session state for user data
- Implement query result caching

### PySpark
- Use Spark for files > 10MB
- Configure memory settings appropriately
- Use broadcast variables for small datasets

---

## Security

### Authentication
- Supabase for authentication
- Session-based auth with timeout
- Password hashing with bcrypt

### Data Validation
- Input validation on all forms
- SQL injection prevention via ORM
- XSS prevention with output escaping

### Access Control
- Role-based permissions
- Export limits per user
- User activity logging

---

## Troubleshooting

### Common Issues

**Import Errors**
- Check column mapping
- Verify CSV format
- Check file size limits

**Database Errors**
- Verify database connection
- Check migration status
- Review error logs

**Performance Issues**
- Enable PySpark for large files
- Optimize queries with indexes
- Use pagination

---

## Contributing

### Development Workflow
1. Create feature branch
2. Implement feature with tests
3. Run tests and linting
4. Submit pull request
5. Code review and merge

### Commit Messages
- Use clear, descriptive messages
- Reference issue numbers
- Use conventional commits format

---

## API Documentation

### Contact Endpoints
- `POST /api/contacts` - Create contact
- `GET /api/contacts/:id` - Get contact
- `PUT /api/contacts/:id` - Update contact
- `DELETE /api/contacts/:id` - Delete contact
- `GET /api/contacts/search` - Search contacts
- `GET /api/contacts/filter` - Filter contacts

### Export Endpoints
- `POST /api/export/all` - Export all
- `POST /api/export/filtered` - Export filtered
- `GET /api/export/history` - Export history

---

## License

MIT License - See LICENSE file for details

