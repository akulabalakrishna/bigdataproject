from kafka import KafkaConsumer
import json

def consume_admissions():
    topic = 'mimic-admissions'
    bootstrap_servers = ['localhost:9092']

    print(f"Connecting to Kafka Consumer at {bootstrap_servers}...")
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='demo-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=10000
        )
        print(f"Connected. Waiting for messages in '{topic}'...")
    except Exception as e:
        print(f"Failed to connect to Kafka Consumer: {e}")
        return

    count = 0
    try:
        for message in consumer:
            count += 1
            # Print minimal info for privacy/demo
            data = message.value
            print(f"Received Record {count}: HADM_ID={data.get('HADM_ID')} | Type={data.get('ADMISSION_TYPE')}")
            
            if count >= 10:
                print("Received 10 samples. Closing consumer.")
                break
    except Exception as e:
        print(f"Error during consumption: {e}")
    finally:
        consumer.close()
        print(f"Test complete. Total records received: {count}")

if __name__ == "__main__":
    consume_admissions()
