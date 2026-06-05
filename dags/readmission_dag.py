from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'icu_readmission_real_pipeline',
    default_args=default_args,
    description='8-Layer Demo: End-to-end real MIMIC-III readmission pipeline',
    schedule_interval=None,
    catchup=False
)

# Project path inside Airflow container
PROJECT_PATH = "/opt/airflow/project"

# 1. Data Availability Check
data_check = BashOperator(
    task_id='data_check',
    bash_command=f'python {PROJECT_PATH}/src/ingestion/data_check.py',
    dag=dag,
)

# 2. Bronze Job (Spark)
# Note: In a real production setup, we would use SparkSubmitOperator or a DockerOperator.
# For the demo, we show the orchestration flow.
bronze_job = BashOperator(
    task_id='bronze_job',
    bash_command='echo "Executing Spark Bronze Job for Real Data Ingestion..." && sleep 5',
    dag=dag,
)

# 3. Silver Job (Spark)
silver_job = BashOperator(
    task_id='silver_job',
    bash_command='echo "Executing Spark Silver Job for Cleaning and Joining..." && sleep 5',
    dag=dag,
)

# 4. Gold Job (Spark)
gold_job = BashOperator(
    task_id='gold_job',
    bash_command='echo "Executing Spark Gold Job for Feature Engineering..." && sleep 5',
    dag=dag,
)

# 5. ML Training
train_model = BashOperator(
    task_id='train_model',
    bash_command=f'python {PROJECT_PATH}/src/training/train.py',
    dag=dag,
)

# Define task dependencies
data_check >> bronze_job >> silver_job >> gold_job >> train_model

