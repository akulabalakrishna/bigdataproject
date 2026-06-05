#!/bin/bash

BASE_DIR="/e/Z5008_Readmission_Project/data/raw/mimiciii"
FILE_LIST="$BASE_DIR/all_mimiciii_files.txt"

if [ ! -f "$FILE_LIST" ]; then
    echo "Error: all_mimiciii_files.txt not found in $BASE_DIR"
    echo "Please run download_mimiciii_full.sh first."
    exit 1
fi

cd "$BASE_DIR" || { echo "Failed to enter directory $BASE_DIR"; exit 1; }

echo "Verifying MIMIC-III files in $BASE_DIR..."
echo "----------------------------------------"

MISSING_COUNT=0
SMALL_COUNT=0

# Files allowed to be small
EXEMPT_FILES="LICENSE.txt README.md SHA256SUMS.txt D_CPT.csv.gz D_LABITEMS.csv.gz all_mimiciii_files.txt"

while IFS= read -r filename; do
    if [ -z "$filename" ]; then continue; fi
    
    if [ ! -f "$filename" ]; then
        echo "[MISSING] $filename"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    else
        # Check size if not exempt
        is_exempt=false
        for exempt in $EXEMPT_FILES; do
            if [ "$filename" == "$exempt" ]; then
                is_exempt=true
                break
            fi
        done

        if [ "$is_exempt" = false ]; then
            size=$(stat -c%s "$filename")
            if [ "$size" -lt 102400 ]; then
                echo "[TOO SMALL] $filename ($(ls -lh "$filename" | awk '{print $5}'))"
                SMALL_COUNT=$((SMALL_COUNT + 1))
            fi
        fi
    fi
done < all_mimiciii_files.txt

echo "----------------------------------------"
if [ $MISSING_COUNT -eq 0 ] && [ $SMALL_COUNT -eq 0 ]; then
    echo "PASS: All files exist and have reasonable sizes."
else
    echo "FAIL: $MISSING_COUNT files missing, $SMALL_COUNT files too small."
fi
