"""
Spark Import Service - High-performance CSV import using PySpark
"""
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, when, trim, lower, regexp_replace, 
    regexp_extract, split, concat_ws, coalesce
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from typing import Dict, List, Optional, Tuple
import re
from services.spark_service import SparkService
from services.csv_column_mapper import CSVColumnMapper


class SparkImportService:
    """Handle large CSV imports using PySpark with validation and deduplication"""
    
    def __init__(self):
        self.spark_service = SparkService()
        self.mapper = CSVColumnMapper()
        
    def is_available(self) -> bool:
        """Check if Spark is available"""
        return self.spark_service.is_available()
    
    def read_csv_with_progress(self, file_path: str, total_rows: int = None) -> DataFrame:
        """Read CSV file with optimized settings for large files"""
        if not self.is_available():
            raise RuntimeError("Spark is not available")
        
        spark = self.spark_service.spark
        
        # Read CSV with optimizations
        df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("timestampFormat", "yyyy-MM-dd HH:mm:ss") \
            .option("dateFormat", "yyyy-MM-dd") \
            .option("encoding", "UTF-8") \
            .option("multiline", "false") \
            .option("escape", "\"") \
            .option("quote", "\"") \
            .option("delimiter", ",") \
            .csv(file_path)
        
        return df
    
    def validate_email(self, df: DataFrame) -> Tuple[DataFrame, DataFrame]:
        """Validate email addresses - returns (valid_df, invalid_df)"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Check if email column exists
        if "email" not in df.columns:
            return df, df.limit(0)  # Return empty for invalid if no email column
        
        # Create validation column
        validated_df = df.withColumn(
            "_email_valid",
            col("email").rlike(email_regex)
        )
        
        # Filter valid records
        valid_df = validated_df.filter(col("_email_valid") == True).drop("_email_valid")
        
        # Filter invalid records
        invalid_df = validated_df.filter(col("_email_valid") == False).drop("_email_valid")
        
        return valid_df, invalid_df
    
    def validate_required_fields(self, df: DataFrame, required_fields: List[str] = None) -> DataFrame:
        """Filter records that have all required fields"""
        if required_fields is None:
            required_fields = ["email", "first_name"]
        
        # Build filter condition
        conditions = [col(field).isNotNull() & (col(field) != "") for field in required_fields if field in df.columns]
        
        if not conditions:
            return df
        
        # Combine all conditions with AND
        combined_condition = conditions[0]
        for condition in conditions[1:]:
            combined_condition = combined_condition & condition
        
        return df.filter(combined_condition)
    
    def clean_data(self, df: DataFrame, column_mapping: Dict[str, str]) -> DataFrame:
        """Clean and normalize data"""
        cleaned_df = df
        
        # Trim whitespace for string columns
        for col_name in df.columns:
            # Use df[col_name] syntax to avoid ambiguous column reference
            cleaned_df = cleaned_df.withColumn(col_name, trim(cleaned_df[col_name]))
        
        # Lowercase emails
        if "email" in cleaned_df.columns:
            cleaned_df = cleaned_df.withColumn("email", lower(col("email")))
        
        # Normalize phone numbers
        if "phone" in cleaned_df.columns:
            # Remove common non-digit characters but keep +
            cleaned_df = cleaned_df.withColumn(
                "phone_cleaned",
                regexp_replace(col("phone"), r'[^\d+]', '')
            )
        
        # Combine first and last name into full_name if not exists
        if "first_name" in cleaned_df.columns and "last_name" in cleaned_df.columns:
            if "full_name" not in cleaned_df.columns:
                cleaned_df = cleaned_df.withColumn(
                    "full_name",
                    trim(concat_ws(" ", col("first_name"), col("last_name")))
                )
        
        return cleaned_df
    
    def deduplicate_by_email(self, df: DataFrame) -> Tuple[DataFrame, DataFrame]:
        """Remove duplicate emails - returns (deduplicated_df, duplicates_df)"""
        if "email" not in df.columns:
            return df, df.limit(0)
        
        # Get duplicates
        duplicates_df = df.groupBy("email").count().filter(col("count") > 1)
        
        # Keep first occurrence based on row number
        from pyspark.sql.window import Window
        from pyspark.sql.functions import row_number
        
        window_spec = Window.partitionBy("email").orderBy(col("email"))
        ranked_df = df.withColumn("row_num", row_number().over(window_spec))
        
        # Keep only first occurrence
        deduplicated_df = ranked_df.filter(col("row_num") == 1).drop("row_num")
        
        return deduplicated_df, duplicates_df
    
    def process_batches(self, df: DataFrame, batch_size: int = 10000) -> List[DataFrame]:
        """Split dataframe into batches for processing"""
        total_rows = df.count()
        batches = []
        
        # Calculate number of partitions needed
        num_partitions = max(1, total_rows // batch_size)
        df = df.repartition(num_partitions)
        
        # Get partition data
        df.cache()
        
        try:
            partitions = df.rdd.glom().collect()
            current_batch = []
            current_count = 0
            
            for partition in partitions:
                for row in partition:
                    current_batch.append(row)
                    current_count += 1
                    
                    if current_count >= batch_size:
                        if current_batch:
                            # Convert batch back to DataFrame
                            batch_df = self.spark_service.spark.createDataFrame(
                                current_batch,
                                schema=df.schema
                            )
                            batches.append(batch_df)
                        current_batch = []
                        current_count = 0
            
            # Add remaining rows
            if current_batch:
                batch_df = self.spark_service.spark.createDataFrame(
                    current_batch,
                    schema=df.schema
                )
                batches.append(batch_df)
        finally:
            df.unpersist()
        
        return batches
    
    def apply_column_mapping(self, df: DataFrame, mapping: Dict[str, str]) -> DataFrame:
        """Apply column mapping to DataFrame"""
        mapped_df = df
        
        # Rename columns based on mapping
        for csv_col, db_field in mapping.items():
            if csv_col in mapped_df.columns:
                mapped_df = mapped_df.withColumnRenamed(csv_col, db_field)
        
        return mapped_df
    
    def process_import(self, file_path: str, column_mapping: Dict[str, str], 
                      batch_size: int = 10000) -> Dict:
        """Process complete import with validation and deduplication"""
        results = {
            'total_rows': 0,
            'valid_rows': 0,
            'invalid_rows': 0,
            'duplicates': 0,
            'batches': [],
            'errors': []
        }
        
        try:
            # Read CSV
            df = self.read_csv_with_progress(file_path)
            results['total_rows'] = df.count()
            
            # Apply column mapping
            mapped_df = self.apply_column_mapping(df, column_mapping)
            
            # Clean data
            cleaned_df = self.clean_data(mapped_df, column_mapping)
            
            # Validate required fields
            validated_df = self.validate_required_fields(cleaned_df, ["email", "first_name"])
            
            # Validate emails
            valid_df, invalid_df = self.validate_email(validated_df)
            results['invalid_rows'] = invalid_df.count()
            
            # Deduplicate
            deduplicated_df, duplicates_df = self.deduplicate_by_email(valid_df)
            results['duplicates'] = duplicates_df.count()
            results['valid_rows'] = deduplicated_df.count()
            
            # Process batches
            batches = self.process_batches(deduplicated_df, batch_size)
            results['batches'] = batches
            
        except Exception as e:
            results['errors'].append(f"Error during import processing: {str(e)}")
        
        return results
    
    def get_preview(self, file_path: str, num_rows: int = 10) -> Optional[DataFrame]:
        """Get preview of CSV file"""
        if not self.is_available():
            return None
        
        try:
            df = self.read_csv_with_progress(file_path)
            return df.limit(num_rows)
        except Exception as e:
            print(f"Error getting preview: {str(e)}")
            return None

