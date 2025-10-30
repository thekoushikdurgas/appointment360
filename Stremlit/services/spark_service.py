"""
Spark Service - Large-scale data processing with PySpark
"""
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, count, avg, max as spark_max, min as spark_min, regexp_extract, trim, lower
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType
from typing import Optional, Dict, List
import os
from config.settings import SPARK_DRIVER_MEMORY, SPARK_EXECUTOR_MEMORY


class SparkService:
    def __init__(self):
        """Initialize Spark session"""
        self.spark = None
        self._create_session()
    
    def _create_session(self):
        """Create Spark session with optimal configuration"""
        try:
            self.spark = SparkSession.builder \
                .appName("ContactManagementSystem") \
                .master("local[*]") \
                .config("spark.driver.memory", SPARK_DRIVER_MEMORY) \
                .config("spark.executor.memory", SPARK_EXECUTOR_MEMORY) \
                .config("spark.sql.shuffle.partitions", "200") \
                .config("spark.sql.adaptive.enabled", "true") \
                .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
                .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
                .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
                .config("spark.sql.files.maxPartitionBytes", "134217728") \
                .config("spark.sql.files.openCostInBytes", "4194304") \
                .getOrCreate()
            
            # Set log level to ERROR to reduce noise
            self.spark.sparkContext.setLogLevel("ERROR")
            
        except Exception as e:
            print(f"Warning: Could not initialize Spark: {str(e)}")
            self.spark = None
    
    def is_available(self) -> bool:
        """Check if Spark is available"""
        return self.spark is not None
    
    def read_csv(self, file_path: str) -> Optional[DataFrame]:
        """Read CSV file into Spark DataFrame"""
        if not self.is_available():
            return None
        
        try:
            df = self.spark.read \
                .option("header", "true") \
                .option("inferSchema", "true") \
                .csv(file_path)
            return df
        except Exception as e:
            print(f"Error reading CSV with Spark: {str(e)}")
            return None
    
    def read_csv_from_bytes(self, file_bytes: bytes, temp_path: str = "/tmp/spark_temp.csv") -> Optional[DataFrame]:
        """Read CSV from bytes into Spark DataFrame"""
        if not self.is_available():
            return None
        
        try:
            # Write bytes to temporary file
            with open(temp_path, 'wb') as f:
                f.write(file_bytes)
            
            # Read with Spark
            df = self.read_csv(temp_path)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return df
        except Exception as e:
            print(f"Error reading CSV from bytes: {str(e)}")
            return None
    
    def process_large_import(self, file_path: str, contact_schema: StructType) -> Optional[DataFrame]:
        """Process large CSV import with Spark"""
        if not self.is_available():
            return None
        
        try:
            # Read with schema for validation
            df = self.spark.read \
                .option("header", "true") \
                .schema(contact_schema) \
                .csv(file_path)
            
            # Data quality checks
            df = self._apply_data_quality_checks(df)
            
            return df
        except Exception as e:
            print(f"Error processing large import: {str(e)}")
            return None
    
    def _apply_data_quality_checks(self, df: DataFrame) -> DataFrame:
        """Apply data quality checks to DataFrame"""
        # Remove rows with missing required fields
        df = df.filter(col("email").isNotNull() & (col("email") != ""))
        
        # Clean email addresses
        df = df.withColumn("email", col("email").lower())
        
        # Remove duplicates based on email
        df = df.dropDuplicates(["email"])
        
        return df
    
    def deduplicate_contacts(self, df: DataFrame, threshold: float = 0.8) -> DataFrame:
        """Identify duplicate contacts using similarity scoring"""
        if not self.is_available():
            return df
        
        # Simple deduplication based on exact matches
        # For fuzzy matching, would use Spark ML similarity functions
        duplicates = df.groupBy("email").count().filter(col("count") > 1)
        
        return duplicates
    
    def analyze_data_quality(self, df: DataFrame) -> Dict:
        """Analyze data quality metrics"""
        if not self.is_available():
            return {}
        
        try:
            total_count = df.count()
            
            # Completeness metrics
            email_completeness = df.filter(col("email").isNotNull() & (col("email") != "")).count() / total_count * 100
            phone_completeness = df.filter(col("phone").isNotNull() & (col("phone") != "")).count() / total_count * 100
            company_completeness = df.filter(col("company").isNotNull() & (col("company") != "")).count() / total_count * 100
            
            # Duplicate count
            duplicate_count = df.groupBy("email").count().filter(col("count") > 1).count()
            
            return {
                'total_records': total_count,
                'email_completeness': email_completeness,
                'phone_completeness': phone_completeness,
                'company_completeness': company_completeness,
                'duplicate_emails': duplicate_count,
                'quality_score': (email_completeness + phone_completeness + company_completeness) / 3
            }
        except Exception as e:
            print(f"Error analyzing data quality: {str(e)}")
            return {}
    
    def aggregate_statistics(self, df: DataFrame) -> Dict:
        """Calculate aggregate statistics"""
        if not self.is_available():
            return {}
        
        try:
            stats = df.agg(
                count("*").alias("total_count"),
                count(when(col("email").isNotNull() & (col("email") != ""), True)).alias("with_email"),
                count(when(col("phone").isNotNull() & (col("phone") != ""), True)).alias("with_phone"),
                count(when(col("company").isNotNull() & (col("company") != ""), True)).alias("with_company")
            ).collect()[0]
            
            return {
                'total': stats['total_count'],
                'email_completeness': (stats['with_email'] / stats['total_count'] * 100) if stats['total_count'] > 0 else 0,
                'phone_completeness': (stats['with_phone'] / stats['total_count'] * 100) if stats['total_count'] > 0 else 0,
                'company_completeness': (stats['with_company'] / stats['total_count'] * 100) if stats['total_count'] > 0 else 0
            }
        except Exception as e:
            print(f"Error calculating statistics: {str(e)}")
            return {}
    
    def export_to_pandas(self, df: DataFrame, limit: int = 10000) -> Optional['pandas.DataFrame']:
        """Convert Spark DataFrame to Pandas DataFrame"""
        if not self.is_available():
            return None
        
        try:
            # Limit rows for memory efficiency
            df_pandas = df.limit(limit).toPandas()
            return df_pandas
        except Exception as e:
            print(f"Error converting to Pandas: {str(e)}")
            return None
    
    def stop(self):
        """Stop Spark session"""
        if self.spark:
            self.spark.stop()
            self.spark = None

