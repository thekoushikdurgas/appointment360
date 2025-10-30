# Django Contact Management System - Pages & Views

## Page Structure

### 1. Authentication Pages

#### Login Page (`/accounts/login/`)
- **Template**: `accounts/login.html`
- **View**: `accounts.views.login_view`
- **Features**:
  - Email/password authentication
  - Supabase integration
  - Password strength indicator
  - Session management
  - Redirect to dashboard after login

#### Signup Page (`/accounts/signup/`)
- **Template**: `accounts/signup.html`
- **View**: `accounts.views.signup_view`
- **Features**:
  - First/last name fields
  - Email validation
  - Password strength meter
  - Password confirmation
  - Create Supabase account
  - Redirect to login

#### Logout
- **View**: `accounts.views.logout_view`
- **Features**:
  - Clear session
  - Logout message
  - Redirect to login

---

### 2. Dashboard Page (`/`)

#### Main Dashboard
- **Template**: `core/dashboard.html`
- **View**: `core.views.dashboard`
- **Features**:
  - 4 metric cards:
    - Total Contacts (orange gradient)
    - Industries (green gradient)
    - Countries (blue gradient)
    - Active Contacts (purple gradient)
  - Industry distribution chart (Plotly horizontal bar)
  - Country distribution chart (Plotly horizontal bar)
  - Quick action buttons:
    - View All Contacts
    - Import Contacts
    - View Analytics

---

### 3. Contact Pages (`/contacts/`)

#### Contact List (`/contacts/`)
- **Template**: `contacts/list.html`
- **View**: `ContactListView` (ListView)
- **Features**:
  - Display contacts in table format
  - Search box (name, company, email)
  - Industry filter (multiselect)
  - Country filter (multiselect)
  - Pagination (25 per page)
  - Edit button for each contact
  - Delete button with confirmation
  - Export button
  - Add Contact button

#### Add Contact (`/contacts/add/`)
- **Template**: `contacts/form.html`
- **View**: `ContactCreateView`
- **Features**:
  - Form with all contact fields
  - Email validation
  - Phone validation
  - URL validation for website/LinkedIn
  - Auto-generate full_name
  - Success message
  - Redirect to list

#### Edit Contact (`/contacts/<id>/edit/`)
- **Template**: `contacts/form.html`
- **View**: `ContactUpdateView`
- **Features**:
  - Pre-filled form
  - Same validation as create
  - Success message
  - Redirect to list

#### Delete Contact (`/contacts/<id>/delete/`)
- **Template**: `contacts/delete_confirm.html`
- **View**: `ContactDeleteView` (DeleteView)
- **Features**:
  - Confirmation dialog
  - Display contact details
  - Success message
  - Redirect to list

#### Export Contacts (POST to `/contacts/export/`)
- **View**: `ContactExportView`
- **Features**:
  - Generate CSV file
  - Apply filters if provided
  - Download file
  - Log export to ExportLog
  - Check export limits

---

### 4. Import Pages (`/imports/`)

#### Upload CSV (`/imports/`)
- **Template**: `imports/upload.html`
- **View**: `imports.views.upload_view`
- **Features**:
  - File upload widget
  - CSV validation
  - File size check
  - Supported formats message
  - Upload button
  - Preview on upload

#### Import Preview (`/imports/`)
- **Template**: `imports/preview.html`
- **Features**:
  - Display first 10 rows
  - Show column mapping
  - Auto-detected mappings highlighted
  - Display column matches
  - Start Import button
  - Cancel button

#### Import Progress (`/imports/progress/<job_id>/`)
- **Template**: `imports/progress.html`
- **View**: `imports.views.progress_view`
- **Features**:
  - Real-time progress bar
  - Processed rows count
  - Success count
  - Error count
  - Duplicate count
  - WebSocket connection for updates
  - Cancel button
  - Auto-refresh every 2 seconds
  - Completion message
  - Navigation buttons (View Contacts, Import Another)

---

### 5. Analytics Pages (`/analytics/`)

#### Analytics Dashboard (`/analytics/`)
- **Template**: `analytics/dashboard.html`
- **View**: `analytics.views.analytics_dashboard`
- **Features**:
  - Key metrics cards
  - Total contacts
  - Active contacts
  - Industry distribution chart
  - Country distribution chart
  - Top companies visualization
  - Growth trend analysis

#### Data Quality (`/analytics/data-quality/`)
- **Template**: `analytics/data_quality.html`
- **View**: `analytics.views.data_quality`
- **Features**:
  - Overall quality score (weighted calculation)
  - Email completeness progress bar
  - Phone completeness progress bar
  - Company completeness progress bar
  - Duplicate email count
  - Missing data counts
  - Quality recommendations
  - Export quality report button

---

### 6. Export Pages (`/exports/`)

#### Export History (`/exports/history/`)
- **Template**: `exports/history.html`
- **View**: `exports.views.export_history`
- **Features**:
  - Export log table
  - Filter by date range
  - Filter by export type
  - Pagination
  - Display export details
  - Record counts
  - Download timestamps

---

### 7. Admin Interface (`/admin/`)

#### Django Admin
- **URL**: `/admin/`
- **Features**:
  - User management
  - Contact management
  - Import job monitoring
  - Export log viewing
  - Advanced filtering
  - Bulk operations
  - Search functionality

---

## URL Patterns

```python
# Root
/  → Dashboard

# Authentication
/accounts/login/  → Login
/accounts/logout/  → Logout
/accounts/signup/  → Sign Up

# Contacts
/contacts/  → Contact List
/contacts/add/  → Add Contact
/contacts/<id>/edit/  → Edit Contact
/contacts/<id>/delete/  → Delete Contact

# Imports
/imports/  → Upload CSV
/imports/progress/<job_id>/  → Import Progress

# Analytics
/analytics/  → Analytics Dashboard
/analytics/data-quality/  → Data Quality

# Exports
/exports/history/  → Export History

# Admin
/admin/  → Django Admin
```

## Navigation Flow

```
Dashboard
    ├── View Contacts → Contact List
    ├── Import Contacts → Import Upload
    └── View Analytics → Analytics Dashboard

Contact List
    ├── Add Contact → Contact Form
    ├── Edit → Contact Form (edit mode)
    ├── Delete → Delete Confirmation
    ├── Export → CSV Download
    └── Search/Filter → Filtered List

Import Upload
    └── Upload → Import Preview → Import Progress

Analytics
    ├── Industry Chart
    ├── Country Chart
    └── Data Quality → Quality Analysis
```

## Template Hierarchy

```
base.html (common layout)
    ├── accounts/
    │   ├── login.html
    │   └── signup.html
    ├── core/
    │   └── dashboard.html
    ├── contacts/
    │   ├── list.html
    │   ├── form.html
    │   └── delete_confirm.html
    └── imports/
        ├── upload.html
        ├── preview.html
        └── progress.html
```

## Component Usage

### Reusable Components

1. **Sidebar** (`components/sidebar.html`)
   - Navigation menu
   - Theme toggle
   - User info
   - Links to all pages

2. **Hero Section** (`components/hero_section.html`)
   - Page title with icon
   - Subtitle
   - Hero actions (buttons)

3. **Metric Cards** (`components/metric_card.html`)
   - Icon
   - Value
   - Label
   - Gradient colors

4. **Progress Tracker** (`components/progress_tracker.html`)
   - Task list
   - WebSocket integration
   - Checkbox tracking

## User Interactions

### Typical User Journey

1. **Login** → Dashboard view
2. **Dashboard** → View statistics
3. **Import** → Upload CSV → Preview → Progress → Complete
4. **Contacts** → View list → Edit/Delete/Export
5. **Analytics** → View charts and quality metrics
6. **Logout** → End session

