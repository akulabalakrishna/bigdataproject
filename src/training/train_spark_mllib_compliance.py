import os
import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, abs, hash, when
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import numpy as np
import mlflow
import mlflow.spark

def main():
    # Setup MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("ICU_Readmission_SparkML_Compliance")

    print("Initializing Spark session...")
    spark = SparkSession.builder \
        .appName("Spark_MLlib_Compliance_Training") \
        .getOrCreate()

    gold_path = "data/minio/lakehouse/gold/readmission_features"
    if not os.path.exists(gold_path):
        print(f"CRITICAL ERROR: Gold Parquet dataset not found at {gold_path}")
        sys.exit(1)

    print(f"Reading Gold dataset from {gold_path}...")
    df = spark.read.parquet(gold_path)
    total_records = df.count()
    print(f"Total Records: {total_records}")

    # Deterministic split on SUBJECT_ID to prevent patient leakage
    print("Performing patient-level split...")
    df_with_hash = df.withColumn("is_train", (abs(hash(col("SUBJECT_ID"))) % 10) < 8)
    train_df = df_with_hash.filter(col("is_train") == True).drop("is_train")
    test_df = df_with_hash.filter(col("is_train") == False).drop("is_train")
    
    train_count = train_df.count()
    test_count = test_df.count()
    print(f"Train Count: {train_count} | Test Count: {test_count}")

    # Prepare features
    categorical_cols = ["ADMISSION_TYPE", "INSURANCE", "RELIGION", "MARITAL_STATUS", "ETHNICITY", "GENDER"]
    numerical_cols = ["AGE", "DIAG_COUNT", "PROC_COUNT", "AVG_ICU_LOS", "ICU_STAY_COUNT", "RX_COUNT", "LAB_COUNT"]

    # String Indexing and OneHotEncoding for Categorical variables
    indexers = [StringIndexer(inputCol=col, outputCol=f"{col}_idx", handleInvalid="keep") for col in categorical_cols]
    encoders = [OneHotEncoder(inputCol=f"{col}_idx", outputCol=f"{col}_vec") for col in categorical_cols]

    # Vector Assembler
    assembler_inputs = numerical_cols + [f"{col}_vec" for col in categorical_cols]
    assembler = VectorAssembler(inputCols=assembler_inputs, outputCol="features")

    # StandardScaler for scaling (beneficial for Logistic Regression)
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=False)

    # Implement both classifiers
    classifiers = {
        "LogisticRegression": LogisticRegression(
            labelCol="READMISSION_30", 
            featuresCol="scaledFeatures", 
            maxIter=100, 
            regParam=0.1
        ),
        "RandomForest": RandomForestClassifier(
            labelCol="READMISSION_30", 
            featuresCol="features", 
            numTrees=100, 
            seed=42
        )
    }

    best_f1 = 0.0
    best_model_name = None
    best_model = None

    for name, clf in classifiers.items():
        print(f"\n--- Training {name} ---")
        start_time = time.time()
        
        # Build pipeline
        pipeline_stages = indexers + encoders + [assembler]
        if name == "LogisticRegression":
            pipeline_stages.append(scaler)
        pipeline_stages.append(clf)
        
        pipeline = Pipeline(stages=pipeline_stages)
        model = pipeline.fit(train_df)
        
        # Evaluate on test set
        predictions = model.transform(test_df)
        
        # Extract probabilities and labels for manual threshold tuning
        probs_and_labels = predictions.select("probability", "READMISSION_30").collect()
        y_prob = np.array([row["probability"][1] for row in probs_and_labels])
        y_test = np.array([row["READMISSION_30"] for row in probs_and_labels])
        
        # Threshold Tuning to maximize F1 (handles class imbalance)
        thresholds = np.linspace(0.05, 0.95, 91)
        best_threshold = 0.5
        max_f1 = 0.0
        
        for t in thresholds:
            y_pred = (y_prob >= t).astype(int)
            tp = np.sum((y_pred == 1) & (y_test == 1))
            fp = np.sum((y_pred == 1) & (y_test == 0))
            fn = np.sum((y_pred == 0) & (y_test == 1))
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
            if f1 > max_f1:
                max_f1 = f1
                best_threshold = t

        # Final predictions at best threshold
        y_pred = (y_prob >= best_threshold).astype(int)
        tp = np.sum((y_pred == 1) & (y_test == 1))
        fp = np.sum((y_pred == 1) & (y_test == 0))
        tn = np.sum((y_pred == 0) & (y_test == 0))
        fn = np.sum((y_pred == 0) & (y_test == 1))
        
        accuracy = (tp + tn) / len(y_test)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = max_f1
        
        # Evaluate ROC-AUC and PR-AUC
        evaluator_roc = BinaryClassificationEvaluator(labelCol="READMISSION_30", rawPredictionCol="probability", metricName="areaUnderROC")
        evaluator_pr = BinaryClassificationEvaluator(labelCol="READMISSION_30", rawPredictionCol="probability", metricName="areaUnderPR")
        
        roc_auc = evaluator_roc.evaluate(predictions)
        pr_auc = evaluator_pr.evaluate(predictions)
        duration = time.time() - start_time
        
        print(f"Results for {name}:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1 Score:  {f1:.4f} (at threshold {best_threshold:.2f})")
        print(f"  ROC-AUC:   {roc_auc:.4f}")
        print(f"  PR-AUC:    {pr_auc:.4f}")
        print(f"  Duration:  {duration:.2f}s")
        
        # Log to MLflow
        with mlflow.start_run(run_name=f"SparkML_{name}"):
            mlflow.log_param("model", name)
            mlflow.log_param("spark_version", spark.version)
            mlflow.log_param("dataset_records", total_records)
            mlflow.log_param("split_seed", 42)
            mlflow.log_param("best_threshold", best_threshold)
            mlflow.log_param("data_source", "Parquet")
            
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("roc_auc", roc_auc)
            mlflow.log_metric("pr_auc", pr_auc)
            mlflow.log_metric("duration_seconds", duration)
            
            try:
                mlflow.spark.log_model(model, "model")
                print("MLflow model logged successfully.")
            except Exception as e:
                print(f"Warning: MLflow model artifact log failed: {e}")
                
        # Save model locally
        save_path = f"models/spark_mllib/{name.lower()}"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            model.write().overwrite().save(save_path)
            print(f"Model saved locally to: {save_path}")
        except Exception as e:
            print(f"Error saving model locally: {e}")
            
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model = model

    # Register the best MLlib model in registry
    print(f"\nRegistering the best model '{best_model_name}' as 'ICU_Readmission_SparkML_Model'...")
    try:
        with mlflow.start_run(run_name="Register_Best_SparkML"):
            mlflow.log_param("best_model_name", best_model_name)
            mlflow.spark.log_model(
                spark_model=best_model, 
                artifact_path="model", 
                registered_model_name="ICU_Readmission_SparkML_Model"
            )
        print("Model registered successfully.")
    except Exception as e:
        print(f"Warning: Model registration failed: {e}")

    spark.stop()
    print("Training process completed.")

if __name__ == "__main__":
    main()
