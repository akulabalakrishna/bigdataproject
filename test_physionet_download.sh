#!/bin/bash

# Configuration
USERNAME="akulabalakrishna0"
TARGET_DIR="/e/Z5008_Readmission_Project/data/raw/mimiciii"
TARGET_FILE="$TARGET_DIR/ADMISSIONS.csv.gz"
URL="https://physionet.org/files/mimiciii/1.4/ADMISSIONS.csv.gz"

# 1. Create folder if missing
mkdir -p "$TARGET_DIR"

# 3. Ask for password interactively
read -s -p "PhysioNet password for $USERNAME: " PHYSIONET_PASS
echo ""

echo "Testing PhysioNet connection with ADMISSIONS.csv.gz..."

# 6-7. Download using curl with specific flags and verbose output
# We use -w "%{http_code}" to capture the status code
HTTP_CODE=$(curl -L --show-error --verbose --user-agent "Wget/1.21.4" \
     -u "$USERNAME:$PHYSIONET_PASS" \
     -w "%{http_code}" \
     -o "$TARGET_FILE" \
     "$URL")

# Clear password from memory as soon as possible
unset PHYSIONET_PASS

echo ""
echo "HTTP Response Code: $HTTP_CODE"

# 10. Handle 403 specifically
if [ "$HTTP_CODE" -eq 403 ]; then
    echo "403 Forbidden. Check PhysioNet username/password, MIMIC-III DUA approval, and command-line access."
    rm -f "$TARGET_FILE"
    exit 1
fi

# Check for other errors
if [ "$HTTP_CODE" -ne 200 ] && [ "$HTTP_CODE" -ne 206 ]; then
    echo "Download failed with HTTP code $HTTP_CODE"
    rm -f "$TARGET_FILE"
    exit 1
fi

# 9. After download, check file size
if [ -f "$TARGET_FILE" ]; then
    SIZE=$(stat -c%s "$TARGET_FILE")
    # 10. If size is less than 1 MB, delete it
    if [ "$SIZE" -lt 1048576 ]; then
        echo "Download failed or returned an HTML/error page (Size: $SIZE bytes)."
        rm -f "$TARGET_FILE"
        exit 1
    else
        # 11. If size is around 2.4 MB, print success
        echo "PhysioNet command-line download test passed."
        echo "File: $TARGET_FILE"
        ls -lh "$TARGET_FILE"
    fi
else
    echo "File was not created. Download failed."
    exit 1
fi
