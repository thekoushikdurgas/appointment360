# Appointment360 Django API Documentation

## Base URL
```
Development: http://localhost:8000
Production: https://yourdomain.com
```

---

## Authentication

All endpoints except authentication endpoints require authentication using session-based authentication.

### Login
**POST** `/api/auth/login/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "user@example.com",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "is_active": true,
    "download_limit": 100
  }
}
```

### Logout
**POST** `/api/auth/logout/`

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

### Password Reset Request
**POST** `/api/auth/password-reset/`

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "If the email exists, a password reset link will be sent"
}
```

### Password Reset Confirm
**POST** `/api/auth/password-reset-confirm/`

**Request Body:**
```json
{
  "token": "reset-token",
  "new_password": "newpassword123",
  "confirm_password": "newpassword123"
}
```

### Get Profile
**GET** `/api/auth/profile/`

**Response:**
```json
{
  "id": 1,
  "username": "user@example.com",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "is_active": true,
  "download_limit": 100,
  "last_login": "2025-01-15T10:30:00Z",
  "date_joined": "2025-01-01T08:00:00Z"
}
```

---

## Contacts

### List Contacts
**GET** `/api/api/contacts/`

**Query Parameters:**
- `name_search` - Search by first or last name
- `location` - Filter by city, state, or country
- `industry` - Filter by industry (can be multiple)
- `email_status` - Filter by email status
- `min_employees` - Minimum employee count
- `max_employees` - Maximum employee count
- `min_revenue` - Minimum annual revenue
- `max_revenue` - Maximum annual revenue
- `technologies` - Search in technologies field
- `page` - Page number (default: 1)
- `page_size` - Results per page (default: 50)

**Example:**
```
GET /api/api/contacts/?name_search=john&industry=Technology&city=New+York
```

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/api/contacts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "full_name": "John Doe",
      "title": "CEO",
      "email": "john@example.com",
      "company": "ABC Corp",
      "city": "New York",
      "country": "USA",
      "industry": "Technology",
      "employees": 500,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

### Get Contact
**GET** `/api/api/contacts/{id}/`

**Response:**
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "title": "CEO",
  "email": "john@example.com",
  "email_status": "Verified",
  "company": "ABC Corp",
  "industry": "Technology",
  "employees": 500,
  "annual_revenue": 5000000.00,
  "city": "New York",
  "state": "NY",
  "country": "USA",
  "person_linkedin_url": "https://linkedin.com/in/johndoe",
  "website": "https://abccorp.com",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

### Create Contact
**POST** `/api/api/contacts/`

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "title": "CTO",
  "email": "jane@example.com",
  "company": "XYZ Inc",
  "industry": "Healthcare",
  "city": "Boston",
  "country": "USA",
  "employees": 200
}
```

### Update Contact
**PUT** `/api/api/contacts/{id}/`

**Request Body:** (Same as Create Contact)

### Delete Contact
**DELETE** `/api/api/contacts/{id}/`

**Response:**
```json
{
  "success": true,
  "message": "Contact deleted successfully"
}
```

### Autocomplete
**GET** `/api/api/contacts/autocomplete/`

**Query Parameters:**
- `field` - Field to search (name, email, company, technologies, keywords, revenue)
- `q` - Search query

**Example:**
```
GET /api/api/contacts/autocomplete/?field=technologies&q=python
```

**Response:**
```json
[
  {"value": "Python"},
  {"value": "Python Django"},
  {"value": "Python Flask"}
]
```

### Export Contacts
**POST** `/api/api/contacts/export/`

**Request Body:**
```json
{
  "contact_ids": [1, 2, 3, 4, 5],
  "fields": ["first_name", "last_name", "email", "company", "city", "country"]
}
```

**Response:**
```json
{
  "success": true,
  "filename": "contacts_export_1.xlsx",
  "file": "data:application/vnd.ms-excel;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

---

## Industries

### List Industries
**GET** `/api/api/industries/`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Technology",
    "description": "Technology sector",
    "is_active": true,
    "created_at": "2025-01-01T08:00:00Z",
    "updated_at": "2025-01-01T08:00:00Z"
  }
]
```

### Get Industry
**GET** `/api/api/industries/{id}/`

---

## Dashboard

### Get Statistics
**GET** `/api/api/dashboard/stats/`

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_contacts": 1500,
    "verified_emails": 1200,
    "unverified_emails": 300,
    "top_industries": [
      {"industry": "Technology", "count": 500},
      {"industry": "Healthcare", "count": 300}
    ],
    "top_countries": [
      {"country": "USA", "count": 800},
      {"country": "UK", "count": 200}
    ],
    "avg_employees": 250.5,
    "total_companies": 1200,
    "avg_revenue": 5000000.00,
    "total_revenue": 7500000000.00,
    "with_linkedin": 1000,
    "recent_contacts": 50
  }
}
```

---

## CSV Upload

### Initialize Upload
**POST** `/api/upload/init/`

**Request Body:**
```json
{
  "fileName": "contacts.csv",
  "fileSize": 10485760,
  "totalChunks": 10
}
```

**Response:**
```json
{
  "success": true,
  "uploadId": "uuid-string",
  "message": "Upload initialized"
}
```

### Upload Chunk
**POST** `/api/upload/chunk/`

**Request:**
- Form Data with fields: `uploadId`, `chunkIndex`, `chunk` (file)

**Response:**
```json
{
  "success": true,
  "message": "Chunk 0 uploaded",
  "uploadedChunks": 1
}
```

### Complete Upload
**POST** `/api/upload/complete/`

**Request Body:**
```json
{
  "uploadId": "uuid-string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "✅ File uploaded successfully. Import job queued.",
  "s3Key": "uploads/uuid-string.csv"
}
```

---

## Payments

### Get Plans
**GET** `/api/payments/plans/`

**Response:**
```json
{
  "success": true,
  "plans": [
    {
      "id": "plan_123",
      "amount": 999,
      "currency": "INR",
      "item": {...}
    }
  ]
}
```

### Create Subscription
**POST** `/api/payments/subscribe/`

**Request Body:**
```json
{
  "plan_id": "plan_123",
  "plan_type": "pro"
}
```

**Response:**
```json
{
  "success": true,
  "subscription": {
    "id": "sub_123",
    "plan_id": "plan_123"
  },
  "subscription_id": "sub_123"
}
```

### Payment Webhook
**POST** `/api/payments/webhook/`

**Headers:**
- `X-Razorpay-Signature` - Webhook signature

**Request Body:**
```json
{
  "event": "payment.captured",
  "payload": {
    "payment": {
      "entity": {...}
    }
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "A server error occurred."
}
```

---

## Authentication Flow

1. User sends login request with email/password
2. Server validates and creates session
3. Client stores session cookie
4. All subsequent requests include session cookie
5. For logout, session is destroyed

---

## Rate Limiting

- Login attempts: 5 per hour per IP
- API requests: 1000 per hour per user
- Upload chunks: No limit
- Export requests: Based on user download limit

---

## Notes

- All timestamps are in UTC ISO 8601 format
- Pagination uses page-based numbering
- Filtering supports multiple values for array fields
- Large file uploads (>10MB) should use chunked upload
- Background job progress can be tracked via Redis

