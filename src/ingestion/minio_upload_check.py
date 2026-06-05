import os
from minio import Minio
from minio.error import S3Error
import io

def check_minio():
    # Configuration
    endpoint = "localhost:9000"
    access_key = "admin"
    secret_key = "adminpassword"
    bucket_name = "mimic-lakehouse"
    
    print(f"Connecting to MinIO at {endpoint}...")
    try:
        client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
        print("MinIO reachable")
    except Exception as e:
        print(f"Failed to connect to MinIO: {e}")
        return

    try:
        # Check if bucket exists
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created")
        else:
            print(f"Bucket '{bucket_name}' exists")

        # Upload a small non-sensitive marker file
        marker_content = "MIMIC-III Real Subset Mode Active. Lakehouse initialized."
        marker_data = io.BytesIO(marker_content.encode('utf-8'))
        
        client.put_object(
            bucket_name,
            "metadata/lakehouse_marker.txt",
            marker_data,
            len(marker_content),
            content_type="text/plain"
        )
        print("Upload successful: metadata/lakehouse_marker.txt")

        # Read proof
        response = client.get_object(bucket_name, "metadata/lakehouse_marker.txt")
        print(f"Read proof success: {response.read().decode('utf-8')}")
        response.close()
        response.release_conn()

    except S3Error as e:
        print(f"S3 Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_minio()
