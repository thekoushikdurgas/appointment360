# Contact Import Setup Guide

## Overview

The high-performance contact import system uses PySpark for processing large CSV files (2GB-5GB+) with PostgreSQL database and background job processing.

## Features

- **High Performance**: Handles large files (2.3GB-4.6GB) efficiently
- **PySpark Powered**: Uses distributed processing for speed
- **PostgreSQL Support**: Optimized for large datasets
- **Background Jobs**: Non-blocking imports with real-time progress
- **Smart Validation**: Email, phone, and required field validation
- **Auto Deduplication**: Removes duplicate emails automatically
- **Column Mapping**: Automatically maps 38 CSV columns to database fields

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_TYPE=postgresql
POSTGRES_HOST=aws-1-ap-southeast-1.pooler.supabase.com
POSTGRES_PORT=6543
POSTGRES_DB=postgres
POSTGRES_USER=postgres.evsjreawstqtkcsbwfjt
POSTGRES_PASSWORD=F5jhYj-X3Wx!nf7
DATABASE_URL=postgresql://postgres.evsjreawstqtkcsbwfjt:F5jhYj-X3Wx!nf7@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres

# PySpark Configuration
SPARK_DRIVER_MEMORY=4g
SPARK_EXECUTOR_MEMORY=4g
IMPORT_BATCH_SIZE=10000
MAX_IMPORT_WORKERS=4
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Key dependencies:
- PySpark 3.5.0+
- SQLAlchemy 2.0.0+
- Streamlit 1.28.0+
- psycopg2-binary (for PostgreSQL)

### 3. Initialize Database

Run the database initialization:

```bash
python scripts/init_db.py
```

This will:
- Create all necessary tables
- Set up indexes for performance
- Configure connection pooling

### 4. Database Migration (if needed)

Note: This application uses PostgreSQL exclusively. No migration from SQLite is needed.

## Usage

### Option 1: Via Streamlit UI (Recommended)

1. Start the Streamlit application:
   ```bash
   streamlit run main.py
   ```

2. Navigate to **"📤 Import Contacts"** page

3. Upload your CSV file (supports files up to 10GB)

4. System will automatically:
   - Detect file size
   - Use PySpark for files >10MB
   - Map columns automatically
   - Start background import

5. Monitor progress in real-time or switch to "📊 Import Progress" page

### Option 2: Command Line Import

For testing or automation:

```python
from services.spark_import_service import SparkImportService
from services.csv_column_mapper import CSVColumnMapper
from services.background_job_service import BackgroundJobService
from config.database import get_db

# Initialize services
spark_service = SparkImportService()
mapper = CSVColumnMapper()
job_service = BackgroundJobService()
db = next(get_db())

# Load CSV and get column mapping
preview = spark_service.get_preview("path/to/file.csv", num_rows=100)
mapping = mapper.auto_map_columns(preview.toPandas())

# Create import job
job = job_service.create_import_job(
    db, "filename.csv", "path/to/file.csv", mapping, user_id=1
)

# Start import
job_service.start_import_job(job.id, "path/to/file.csv", mapping)
```

### Option 3: Direct Import (Small Files)

For small files (<10MB), traditional Pandas import:

```python
from services.csv_service import CSVService
from services.contact_service import ContactService
from config.database import get_db

csv_service = CSVService()
contact_service = ContactService(next(get_db()))

# Read and import
df = csv_service.read_csv("path/to/file.csv")
chunks = csv_service.process_chunks(df, chunk_size=1000)

for chunk in chunks:
    # Process each chunk
    contact_service.bulk_create(chunk)
```

## Performance Benchmarking

Run benchmarks to test import speed:

```bash
python scripts/benchmark_import.py data/3519363_1M.csv
```

This will show:
- File size and row count
- Read speed (rows/second)
- Validation performance
- Deduplication statistics
- Batch processing metrics
- Estimated database insert time

## CSV Format

### Supported Columns

The system automatically maps these CSV columns:

**Personal Information:**
- first_name, last_name, full_name
- email, phone (work_direct_phone, home_phone, mobile_phone, corporate_phone, other_phone)
- title, seniority

**Company Information:**
- company, company_name_for_emails
- industry, employees, company_size
- annual_revenue, total_funding, latest_funding_amount
- keywords, technologies, departments

**Location:**
- city, state, country, postal_code
- company_city, company_state, company_country
- company_address, company_phone

**Social Media:**
- person_linkedin_url, company_linkedin_url
- facebook_url, twitter_url
- website

### Required Fields

Minimum required for import:
- email (must be valid)
- first_name

All other fields are optional.

## Performance Metrics

### Expected Performance

For a 1M row CSV (2.3GB):
- Read: ~10-20 seconds
- Validation: ~5-10 seconds
- Deduplication: ~3-5 seconds
- Batch creation: ~2-3 seconds
- Database insert: ~20-30 seconds
- **Total: ~40-70 seconds**

For a 2M row CSV (4.6GB):
- Read: ~20-40 seconds
- Validation: ~10-20 seconds
- Deduplication: ~6-10 seconds
- Batch creation: ~4-6 seconds
- Database insert: ~40-60 seconds
- **Total: ~80-140 seconds**

### Optimization Tips

1. **Increase Memory** (if you have RAM):
   ```env
   SPARK_DRIVER_MEMORY=8g
   SPARK_EXECUTOR_MEMORY=8g
   ```

2. **Adjust Batch Size** (faster processing, more memory):
   ```env
   IMPORT_BATCH_SIZE=50000
   ```

3. **Reduce Batch Size** (less memory, slower):
   ```env
   IMPORT_BATCH_SIZE=5000
   ```

## Troubleshooting

### Issue: "Spark is not available"

**Solution**: Install PySpark
```bash
pip install pyspark
```

### Issue: Slow import performance

**Solutions**:
1. Check Spark memory settings
2. Reduce batch size if running out of memory
3. Verify PostgreSQL connection settings
4. Check network connection to database

### Issue: Out of memory errors

**Solutions**:
1. Reduce `IMPORT_BATCH_SIZE`
2. Increase `SPARK_DRIVER_MEMORY` and `SPARK_EXECUTOR_MEMORY`
3. Process file in smaller chunks manually

### Issue: Column mapping not working

**Solutions**:
1. Check CSV column names
2. Update `services/csv_column_mapper.py` with new column patterns
3. Verify CSV encoding is UTF-8

## Monitoring

### View Import Jobs

Navigate to **"📊 Import Progress"** page to see:
- Current job status
- Progress percentage
- Rows processed vs total
- Success/error counts
- Processing speed
- Estimated completion time

### Error Reports

If import fails:
1. Check error count in progress page
2. Download error report (if available)
3. Review column mapping
4. Check CSV format and encoding

## Advanced Usage

### Custom Column Mapping

If auto-mapping doesn't work:

```python
mapping = {
    'csv_column_name': 'database_field',
    'email': 'email',
    'name': 'first_name',
    # ... add more mappings
}
```

### Validation Rules

Strict validation is enabled by default:
- Email format: Standard email regex
- Required fields: email, first_name
- Phone format: Any (kept as-is)

To disable validation (not recommended):
```python
# Modify services/spark_import_service.py
# Comment out validation steps
```

## Database Schema

See `models/contact.py` for complete schema including:
- Standard fields (name, email, phone, etc.)
- Extended fields (revenue, funding, seniority, etc.)
- Social media URLs
- Company information
- Indexes for performance

## Support

For issues or questions:
1. Check logs in console output
2. Review error messages in progress page
3. Run benchmark to identify bottlenecks
4. Check database connection settings

