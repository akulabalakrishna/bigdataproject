import os
import sys
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
import mlflow
import mlflow.spark

def main():
    spark = SparkSession.builder \
        .appName("ICU_Readmission_Spark_MLlib") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    gold_path = "data/minio/lakehouse/gold/readmission_features"
    if not os.path.exists(gold_path):
        print(f"Error: Gold features not found at {gold_path}. Please run Bronze, Silver, and Gold ETL jobs first.")
        sys.exit(1)

    print(f"Loading Gold features from: {gold_path}")
    df = spark.read.parquet(gold_path)

    # Identify target column safely
    target_candidates = ["readmission_30d", "READMISSION_30D", "label", "target"]
    target_col = None
    for col in target_candidates:
        if col in df.columns:
            target_col = col
            break

    if not target_col:
        print(f"Error: Could not find a valid binary target column. Candidates checked: {target_candidates}")
        sys.exit(1)

    print(f"Target column identified: {target_col}")

    # Identify feature columns (exclude IDs and target)
    exclude_cols = [target_col, 'SUBJECT_ID', 'HADM_ID', 'subject_id', 'hadm_id']
    feature_cols = [c for c in df.columns if c not in exclude_cols]

    # Handle numeric vs categorical features safely
    # For a robust implementation, we will assemble all numeric features.
    # If categorical strings exist, they must be StringIndexed.
    numeric_cols = [f.name for f in df.schema.fields if isinstance(f.dataType, (pyspark.sql.types.DoubleType, pyspark.sql.types.IntegerType, pyspark.sql.types.FloatType, pyspark.sql.types.LongType)) and f.name in feature_cols]
    
    # Simple vector assembler for numeric data (assuming upstream Gold ETL handled categoricals via OHE)
    assembler = VectorAssembler(inputCols=numeric_cols, outputCol="features", handleInvalid="skip")
    assembled_df = assembler.transform(df)

    # Ensure target column is a numeric label for MLlib
    assembled_df = assembled_df.withColumn("label", assembled_df[target_col].cast("double"))

    # Train/Test split
    train_df, test_df = assembled_df.randomSplit([0.8, 0.2], seed=42)
    print(f"Training records: {train_df.count()}, Testing records: {test_df.count()}")

    mlflow.set_experiment("ICU_Readmission_Spark_MLlib")

    models = [
        ("LogisticRegression", LogisticRegression(featuresCol="features", labelCol="label", maxIter=10)),
        ("RandomForestClassifier", RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=20)),
        ("GBTClassifier", GBTClassifier(featuresCol="features", labelCol="label", maxIter=10))
    ]

    auc_evaluator = BinaryClassificationEvaluator(labelCol="label", metricName="areaUnderROC")
    acc_evaluator = MulticlassClassificationEvaluator(labelCol="label", metricName="accuracy")

    best_auc = 0.0
    best_model_name = None

    for name, model_cls in models:
        print(f"\nTraining {name}...")
        with mlflow.start_run(run_name=name):
            model = model_cls.fit(train_df)
            predictions = model.transform(test_df)

            auc = auc_evaluator.evaluate(predictions)
            acc = acc_evaluator.evaluate(predictions)

            print(f"Model: {name} | AUC: {auc:.4f} | Accuracy: {acc:.4f}")

            mlflow.log_param("model_type", name)
            mlflow.log_param("feature_count", len(numeric_cols))
            mlflow.log_metric("auc", auc)
            mlflow.log_metric("accuracy", acc)

            # Attempt to log Spark model artifact
            try:
                mlflow.spark.log_model(model, "spark_model")
            except Exception as e:
                print(f"Warning: Could not log Spark artifact to MLflow: {e}")

            if auc > best_auc:
                best_auc = auc
                best_model_name = name

    print(f"\nBest Model: {best_model_name} with AUC: {best_auc:.4f}")
    spark.stop()

if __name__ == "__main__":
    import pyspark
    main()
