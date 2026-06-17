# Airflow DAG Evidence

The Airflow scheduler successfully registered the main orchestration DAG.

**Command Executed:**
```bash
docker exec z5008_readmission_project-airflow-webserver-1 airflow dags list
```

**Results:**
```text
dag_id                        | filepath           | owner   | paused
==============================+====================+=========+=======
icu_readmission_real_pipeline | readmission_dag.py | airflow | True  
```

The DAG is fully loaded in the Airflow metadata database and is ready to orchestrate the Bronze -> Silver -> Gold -> Train sequence on a schedule.
