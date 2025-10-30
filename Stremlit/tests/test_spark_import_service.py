"""
Tests for Spark Import Service
"""
import pytest
import pandas as pd
from services.spark_import_service import SparkImportService


@pytest.fixture
def spark_service():
    """Create spark import service instance"""
    return SparkImportService()


def test_email_validation(spark_service):
    """Test email validation"""
    if not spark_service.is_available():
        pytest.skip("Spark not available")
    
    spark = spark_service.spark_service.spark
    
    # Create test dataframe
    data = [
        ("valid@email.com",),
        ("invalid-email",),
        ("another.valid@domain.co.uk",),
        ("invalid@",),
        ("@invalid.com",),
        ("valid+tag@email.com",),
    ]
    
    df = spark.createDataFrame(data, ["email"])
    
    # Validate emails
    valid_df, invalid_df = spark_service.validate_email(df)
    
    # Should have 3 valid and 3 invalid
    assert valid_df.count() == 3
    assert invalid_df.count() == 3


def test_required_fields_validation(spark_service):
    """Test required fields validation"""
    if not spark_service.is_available():
        pytest.skip("Spark not available")
    
    spark = spark_service.spark_service.spark
    
    # Create test dataframe
    data = [
        ("John", "john@email.com"),
        ("Jane", ""),
        ("", "jane@email.com"),
        ("Bob", "bob@email.com"),
    ]
    
    df = spark.createDataFrame(data, ["first_name", "email"])
    
    # Validate required fields
    validated_df = spark_service.validate_required_fields(df, ["first_name", "email"])
    
    # Should only have records with both fields
    assert validated_df.count() == 2


def test_deduplicate_by_email(spark_service):
    """Test email deduplication"""
    if not spark_service.is_available():
        pytest.skip("Spark not available")
    
    spark = spark_service.spark_service.spark
    
    # Create test dataframe with duplicates
    data = [
        ("John", "john@email.com"),
        ("Jane", "jane@email.com"),
        ("Bob", "john@email.com"),  # Duplicate
        ("Alice", "jane@email.com"),  # Duplicate
    ]
    
    df = spark.createDataFrame(data, ["name", "email"])
    
    # Deduplicate
    deduplicated_df, duplicates_df = spark_service.deduplicate_by_email(df)
    
    # Should have 2 unique emails
    assert deduplicated_df.count() == 2
    assert duplicates_df.count() == 2  # 2 duplicate groups


def test_data_cleaning(spark_service):
    """Test data cleaning functionality"""
    if not spark_service.is_available():
        pytest.skip("Spark not available")
    
    spark = spark_service.spark_service.spark
    
    # Create test dataframe with whitespace
    data = [
        ("  John  ", "  John@Email.COM  ", "  Company  "),
        ("  Jane  ", "  JANE@email.com  ", "  Corp  "),
    ]
    
    df = spark.createDataFrame(data, ["first_name", "email", "company"])
    
    # Clean data
    mapping = {"first_name": "first_name", "email": "email", "company": "company"}
    cleaned_df = spark_service.clean_data(df, mapping)
    
    # Check that data is cleaned (converted to lower case for email)
    rows = cleaned_df.collect()
    for row in rows:
        assert row['email'] == row['email'].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

