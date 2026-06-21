import os
import sys
from pyspark.sql import SparkSession

def main():
    # Read MinIO credentials from env
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    
    if not aws_access_key or not aws_secret_key:
        print("CRITICAL ERROR: AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY is not set.")
        sys.exit(1)
        
    print("Initializing Spark session with Iceberg configurations...")
    spark = SparkSession.builder \
        .appName("Migrate_Parquet_to_Iceberg") \
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
        .config("spark.sql.catalog.lakehouse", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.lakehouse.type", "hadoop") \
        .config("spark.sql.catalog.lakehouse.warehouse", "s3a://lakehouse/iceberg-warehouse") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key) \
        .getOrCreate()

    # Define migrations mapping: (source_parquet_path, iceberg_table_name, namespace)
    migrations = [
        ("data/minio/lakehouse/bronze/mimiciii/ADMISSIONS", "lakehouse.bronze.admissions", "lakehouse.bronze"),
        ("data/minio/lakehouse/silver/mimiciii/ADMISSIONS_CLEANED", "lakehouse.silver.admissions_cleaned", "lakehouse.silver"),
        ("data/minio/lakehouse/gold/readmission_features", "lakehouse.gold.readmission_features", "lakehouse.gold")
    ]
    
    overall_status = "PASS"
    
    for src_path, dest_table, namespace in migrations:
        print("="*60)
        print(f"Migrating Parquet from: {src_path}")
        print(f"To Iceberg Table:        {dest_table}")
        
        try:
            if not os.path.exists(src_path):
                raise FileNotFoundError(f"Source Parquet path not found: {src_path}")
                
            # Read Parquet source
            df = spark.read.parquet(src_path)
            src_count = df.count()
            print(f"Source Record Count:    {src_count}")
            
            # Create namespace if not exists
            spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {namespace}")
            
            # Write to Iceberg
            df.writeTo(dest_table).using("iceberg").createOrReplace()
            
            # Verify destination count and format
            dest_df = spark.read.table(dest_table)
            dest_count = dest_df.count()
            print(f"Destination Record Count: {dest_count}")
            
            # Verify Iceberg table metadata/provider
            details_df = spark.sql(f"DESCRIBE EXTENDED {dest_table}")
            provider_row = details_df.filter("col_name = 'Provider'").select("data_type").first()
            provider_str = provider_row[0] if provider_row else "unknown"
            print(f"Table Provider:          {provider_str}")
            
            location_row = details_df.filter("col_name = 'Location'").select("data_type").first()
            location_str = location_row[0] if location_row else "unknown"
            print(f"MinIO Warehouse Path:    {location_str}")
            
            if src_count == dest_count and "iceberg" in provider_str.lower():
                print(f"Migration Status:        PASS")
            else:
                print(f"Migration Status:        FAIL (count discrepancy or provider is not Iceberg)")
                overall_status = "FAIL"
                
        except Exception as e:
            print(f"CRITICAL ERROR migrating {src_path}: {e}")
            overall_status = "FAIL"
            
    print("="*60)
    print(f"FINAL MIGRATION PIPELINE STATUS: {overall_status}")
    spark.stop()
    
    if overall_status == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
