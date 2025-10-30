"""
Performance Benchmarking Script
Benchmark import performance with large CSV files
"""
import time
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.spark_import_service import SparkImportService
from services.csv_column_mapper import CSVColumnMapper
from config.settings import IMPORT_BATCH_SIZE


def benchmark_import(file_path: str):
    """Benchmark import performance"""
    print("=" * 80)
    print("🚀 Performance Benchmark - Contact Import")
    print("=" * 80)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    # Get file size
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / 1024 / 1024
    
    print(f"\n📁 File: {file_path}")
    print(f"📊 Size: {file_size_mb:.2f} MB")
    
    # Initialize services
    spark_service = SparkImportService()
    mapper = CSVColumnMapper()
    
    if not spark_service.is_available():
        print("❌ Spark is not available")
        return
    
    # Read and analyze
    print("\n" + "=" * 80)
    print("📖 Phase 1: Reading CSV")
    print("=" * 80)
    start_time = time.time()
    
    df = spark_service.read_csv_with_progress(file_path)
    total_rows = df.count()
    
    read_time = time.time() - start_time
    rows_per_second = total_rows / read_time if read_time > 0 else 0
    
    print(f"✅ Read {total_rows:,} rows in {read_time:.2f} seconds")
    print(f"⚡ Speed: {rows_per_second:,.0f} rows/second")
    
    # Get column mapping
    print("\n" + "=" * 80)
    print("🗺️ Phase 2: Column Mapping")
    print("=" * 80)
    start_time = time.time()
    
    preview_df = spark_service.get_preview(file_path, num_rows=100)
    if preview_df:
        df_pandas = preview_df.toPandas()
        mapping = mapper.auto_map_columns(df_pandas)
        
        mapping_time = time.time() - start_time
        
        print(f"✅ Mapped {len(mapping)} columns in {mapping_time:.2f} seconds")
        print("Mappings:")
        for csv_col, db_field in list(mapping.items())[:10]:
            print(f"  - {csv_col} → {db_field}")
    
    # Validation
    print("\n" + "=" * 80)
    print("✓ Phase 3: Validation")
    print("=" * 80)
    start_time = time.time()
    
    # Apply mapping
    mapped_df = spark_service.apply_column_mapping(df, mapping)
    
    # Clean data
    cleaned_df = spark_service.clean_data(mapped_df, mapping)
    
    # Validate required fields
    validated_df = spark_service.validate_required_fields(cleaned_df, ["email", "first_name"])
    
    validation_time = time.time() - start_time
    valid_rows = validated_df.count()
    
    print(f"✅ Validated {valid_rows:,} rows in {validation_time:.2f} seconds")
    print(f"⚡ Speed: {valid_rows / validation_time:,.0f} rows/second")
    print(f"📊 Validation rate: {(valid_rows / total_rows * 100):.2f}%")
    
    # Deduplication
    print("\n" + "=" * 80)
    print("🔄 Phase 4: Deduplication")
    print("=" * 80)
    start_time = time.time()
    
    deduplicated_df, duplicates_df = spark_service.deduplicate_by_email(validated_df)
    unique_rows = deduplicated_df.count()
    duplicate_count = duplicates_df.count()
    
    dedupe_time = time.time() - start_time
    
    print(f"✅ Found {duplicate_count:,} duplicate email groups")
    print(f"✅ {unique_rows:,} unique contacts after deduplication")
    print(f"⚡ Deduplication completed in {dedupe_time:.2f} seconds")
    
    # Batch processing
    print("\n" + "=" * 80)
    print("📦 Phase 5: Batch Processing")
    print("=" * 80)
    start_time = time.time()
    
    batches = spark_service.process_batches(deduplicated_df, batch_size=IMPORT_BATCH_SIZE)
    
    batch_time = time.time() - start_time
    
    print(f"✅ Created {len(batches)} batches")
    print(f"⚡ Batch creation completed in {batch_time:.2f} seconds")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    total_time = read_time + mapping_time + validation_time + dedupe_time + batch_time
    
    print(f"Total Rows Processed: {total_rows:,}")
    print(f"Valid Rows: {valid_rows:,} ({valid_rows/total_rows*100:.2f}%)")
    print(f"Unique Contacts: {unique_rows:,}")
    print(f"Duplicates: {duplicate_count:,}")
    print(f"Batches Created: {len(batches)}")
    print(f"\n⏱️ Total Processing Time: {total_time:.2f} seconds")
    print(f"⚡ Average Speed: {unique_rows/total_time:,.0f} rows/second")
    print(f"📈 Throughput: {file_size_mb/total_time:.2f} MB/second")
    
    # Estimated database import time (assuming 10,000 rows/second for inserts)
    estimated_insert_time = unique_rows / 10000
    print(f"\n💾 Estimated DB Insert Time: {estimated_insert_time:.2f} seconds")
    print(f"⏱️ Total Estimated Time: {total_time + estimated_insert_time:.2f} seconds")
    
    print("\n" + "=" * 80)


def main():
    """Main benchmark function"""
    # Check if file path provided
    if len(sys.argv) < 2:
        print("Usage: python benchmark_import.py <path_to_csv_file>")
        print("\nExample:")
        print("  python benchmark_import.py data/3519363_1M.csv")
        return
    
    file_path = sys.argv[1]
    benchmark_import(file_path)


if __name__ == "__main__":
    main()

