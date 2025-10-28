# Contact Management System

A modern contact management system built with Streamlit, PostgreSQL, and Supabase.

## 🚀 Features

- **Dashboard** - Overview statistics and quick actions
- **Contact Management** - Full CRUD operations with advanced filtering
- **CSV Import** - Chunked processing for large files with column mapping
- **CSV Export** - Export to Excel/CSV with download limits
- **User Management** - Role-based access control
- **Settings** - User preferences and configuration
- **Analytics** - Data visualization and insights
- **Data Quality** - Quality scoring and validation

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Supabase account (for authentication)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd contact-management-system
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

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database and Supabase credentials
```

5. **Initialize database**
```bash
python scripts/init_db.py
```

## 🎯 Usage

Run the application:
```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

### Default Login
- Email: admin@example.com
- Password: admin123

## 📁 Project Structure

```
.
├── config/          # Configuration files
├── models/          # Database models
├── services/        # Business logic services
├── pages/           # Streamlit pages
├── components/      # Reusable components
├── utils/           # Utility functions
├── tests/           # Test files
├── scripts/         # Utility scripts
├── main.py         # Application entry point
└── requirements.txt # Python dependencies
```

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

## 📝 License

MIT License

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
