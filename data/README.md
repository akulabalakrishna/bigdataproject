# Data Directory

> [!WARNING]
> **Data Privacy Rules**
> 
> The raw MIMIC-III dataset contains restricted clinical data and is **NOT** included in this repository.
> 
> All subdirectories (`raw/`, `bronze/`, `silver/`, `gold/`) are ignored by Git.

## How to Obtain the Data
1. You must be a credentialed user on PhysioNet.
2. Complete the required CITI training.
3. Sign the Data Use Agreement (DUA) for MIMIC-III.
4. Download the dataset directly from [PhysioNet MIMIC-III v1.4](https://physionet.org/content/mimiciii/1.4/).

Once downloaded, place the `.csv.gz` files in `data/raw/mimiciii/` before running the pipeline.
