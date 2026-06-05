#!/bin/bash

# Configuration
USERNAME="akulabalakrishna0"
BASE_DIR="/e/Z5008_Readmission_Project/data/raw/mimiciii"
URL_PREFIX="https://physionet.org/files/mimiciii/1.4"

# 1. Create folder if missing
mkdir -p "$BASE_DIR"

# 2. cd into directory
cd "$BASE_DIR" || { echo "Failed to enter directory $BASE_DIR"; exit 1; }

# 3. Remove tiny failed downloads (< 100 KB) for specific files
echo "Cleaning up tiny failed downloads if any..."
for f in ADMISSIONS.csv.gz PATIENTS.csv.gz mimic-iii-clinical-database-1.4.zip; do
    if [ -f "$f" ]; then
        size=$(stat -c%s "$f")
        if [ "$size" -lt 102400 ]; then
            echo "Removing failed/tiny file: $f ($size bytes)"
            rm "$f"
        fi
    fi
done

# 4. Create file list
echo "Creating file list..."
cat <<EOF > all_mimiciii_files.txt
ADMISSIONS.csv.gz
CALLOUT.csv.gz
CAREGIVERS.csv.gz
CHARTEVENTS.csv.gz
CPTEVENTS.csv.gz
DATETIMEEVENTS.csv.gz
DIAGNOSES_ICD.csv.gz
DRGCODES.csv.gz
D_CPT.csv.gz
D_ICD_DIAGNOSES.csv.gz
D_ICD_PROCEDURES.csv.gz
D_ITEMS.csv.gz
D_LABITEMS.csv.gz
ICUSTAYS.csv.gz
INPUTEVENTS_CV.csv.gz
INPUTEVENTS_MV.csv.gz
LABEVENTS.csv.gz
LICENSE.txt
MICROBIOLOGYEVENTS.csv.gz
NOTEEVENTS.csv.gz
OUTPUTEVENTS.csv.gz
PATIENTS.csv.gz
PRESCRIPTIONS.csv.gz
PROCEDUREEVENTS_MV.csv.gz
PROCEDURES_ICD.csv.gz
README.md
SERVICES.csv.gz
SHA256SUMS.txt
TRANSFERS.csv.gz
EOF

# 5. Ask for password
read -s -p "PhysioNet password for $USERNAME: " PHYSIONET_PASS
echo ""

# --- CONNECTION TEST START ---
echo "Testing connection with ADMISSIONS.csv.gz before starting full download..."
TEST_FILE="ADMISSIONS.csv.gz"
HTTP_CODE=$(curl -L --show-error --user-agent "Wget/1.21.4" \
     -u "$USERNAME:$PHYSIONET_PASS" \
     -w "%{http_code}" \
     -o "$TEST_FILE" \
     "$URL_PREFIX/$TEST_FILE")

if [ "$HTTP_CODE" -eq 403 ]; then
    echo "403 Forbidden. Check PhysioNet username/password, MIMIC-III DUA approval, and command-line access."
    unset PHYSIONET_PASS
    exit 1
fi

if [ "$HTTP_CODE" -ne 200 ] && [ "$HTTP_CODE" -ne 206 ]; then
    echo "Initial test failed with HTTP code $HTTP_CODE. Stopping."
    unset PHYSIONET_PASS
    exit 1
fi

SIZE=$(stat -c%s "$TEST_FILE" 2>/dev/null || echo 0)
if [ "$SIZE" -lt 1048576 ]; then
    echo "Initial test file is too small ($SIZE bytes). Likely an error page. Stopping."
    unset PHYSIONET_PASS
    exit 1
fi

echo "Connection test passed. Starting full download..."
# --- CONNECTION TEST END ---

# 6-9. Download loop
while IFS= read -r filename; do
    if [ -z "$filename" ]; then continue; fi
    
    # Skip ADMISSIONS if it was just downloaded in the test
    # (Though curl -C - would handle it anyway, it's cleaner to be explicit)
    
    echo "----------------------------------------"
    echo "Downloading $filename..."
    
    # We capture HTTP code in the loop too to catch 403s on later files
    HTTP_CODE=$(curl -L --show-error -C - --retry 20 --retry-delay 20 \
         --user-agent "Wget/1.21.4" \
         -u "$USERNAME:$PHYSIONET_PASS" \
         -w "%{http_code}" \
         "$URL_PREFIX/$filename" -o "$filename")
    
    if [ "$HTTP_CODE" -eq 403 ]; then
        echo "403 Forbidden encountered while downloading $filename. Stopping."
        unset PHYSIONET_PASS
        exit 1
    fi

    echo "Download status for $filename (HTTP $HTTP_CODE):"
    ls -lh "$filename"
done < all_mimiciii_files.txt

# Clear password variable
unset PHYSIONET_PASS

# 10. Verify important file sizes
echo "----------------------------------------"
echo "Verifying important file sizes:"
echo "Expected: ADMISSIONS.csv.gz ~2.4 MB"
ls -lh ADMISSIONS.csv.gz 2>/dev/null || echo "ADMISSIONS.csv.gz MISSING"

echo "Expected: PATIENTS.csv.gz ~558 KB"
ls -lh PATIENTS.csv.gz 2>/dev/null || echo "PATIENTS.csv.gz MISSING"

echo "Expected: CHARTEVENTS.csv.gz ~4 GB"
ls -lh CHARTEVENTS.csv.gz 2>/dev/null || echo "CHARTEVENTS.csv.gz MISSING"

echo "Expected: LABEVENTS.csv.gz ~320 MB"
ls -lh LABEVENTS.csv.gz 2>/dev/null || echo "LABEVENTS.csv.gz MISSING"

# 11. Total folder size
echo "----------------------------------------"
echo "Total folder size:"
du -sh .

# 12. Final message
echo "----------------------------------------"
echo "MIMIC-III full dataset download attempt completed. Check file sizes before running real pipeline."
