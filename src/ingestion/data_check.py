import os
import sys

def check_mimic_files():
    base_path = "E:/Z5008_Readmission_Project/data/raw/mimiciii/"
    
    mandatory_files = [
        "ADMISSIONS.csv.gz",
        "PATIENTS.csv.gz"
    ]
    
    complete_subset_files = [
        "DIAGNOSES_ICD.csv.gz",
        "PROCEDURES_ICD.csv.gz",
        "ICUSTAYS.csv.gz",
        "D_ICD_DIAGNOSES.csv.gz",
        "D_ITEMS.csv.gz",
        "D_LABITEMS.csv.gz"
    ]
    
    incomplete_optional_files = [
        "LABEVENTS.csv.gz",
        "PRESCRIPTIONS.csv.gz",
        "CHARTEVENTS.csv.gz"
    ]
    
    missing_mandatory = [f for f in mandatory_files if not os.path.exists(os.path.join(base_path, f))]
    available_complete = [f for f in complete_subset_files if os.path.exists(os.path.join(base_path, f))]
    missing_complete = [f for f in complete_subset_files if not os.path.exists(os.path.join(base_path, f))]
    missing_incomplete = [f for f in incomplete_optional_files if not os.path.exists(os.path.join(base_path, f))]
    
    if missing_mandatory:
        print("="*60)
        print("CRITICAL ERROR: Mandatory Real MIMIC-III files missing.")
        print(f"Missing Mandatory: {', '.join(missing_mandatory)}")
        print("Ensure ADMISSIONS and PATIENTS are downloaded to the raw folder.")
        print("="*60)
        return False
    else:
        print("="*60)
        print("REAL SUBSET MODE ACTIVE")
        print("-" * 60)
        print(f"Mandatory files found: {', '.join(mandatory_files)}")
        print(f"Available complete subset files: {', '.join(available_complete) if available_complete else 'None'}")
        
        if missing_complete:
            print(f"Missing complete subset files (optional): {', '.join(missing_complete)}")
            
        print("-" * 60)
        print("WARNING: Incomplete/Missing optional large event tables:")
        for f in incomplete_optional_files:
            status = "Incomplete/Skipped" if f in ["LABEVENTS.csv.gz", "PRESCRIPTIONS.csv.gz"] else "Not Available"
            print(f"- {f}: {status}")
            
        print("="*60)
        return True

if __name__ == "__main__":
    is_real = check_mimic_files()
    if not is_real:
        sys.exit(1)

