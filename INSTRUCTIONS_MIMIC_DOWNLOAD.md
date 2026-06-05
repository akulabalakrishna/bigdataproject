# MIMIC-III v1.4 Download Instructions (Official Wget Method)

Since `curl` may encounter 403 Forbidden errors due to user-agent or security policies, we use the official PhysioNet recommended `wget` method.

## 1. Setup Environment
**Path:** `E:\Z5008_Readmission_Project\data\raw\mimiciii\`

In Git Bash, navigate to your project data folder:
```bash
cd /e/Z5008_Readmission_Project/data/raw/mimiciii
```

## 2. Download Command
Run the following command to download the full dataset:
```bash
wget -r -N -c -np --user akulabalakrishna0 --ask-password https://physionet.org/files/mimiciii/1.4/
```
- `-r`: Recursive download.
- `-N`: Only retrieve files newer than local ones.
- `-c`: Continue getting a partially-downloaded file.
- `-np`: Do not ascend to the parent directory.
- `--user`: Your PhysioNet username.
- `--ask-password`: Prompts for your password securely.

## 3. Troubleshooting & Notes

### If `wget` is not found
If you get `command not found: wget`:
1. **Install wget**: Download the `wget.exe` for Windows or use a package manager like `choco install wget`.
2. **Environment Path**: Ensure `wget` is in your Windows PATH.
3. **Restart Terminal**: Close and reopen Git Bash after installation.

### Handling Nested Folders
If `wget` downloads files into a nested structure like `physionet.org/files/mimiciii/1.4/`:
1. Move the `.csv.gz` files directly into `/e/Z5008_Readmission_Project/data/raw/mimiciii/`.
2. You can use this command in Git Bash:
   ```bash
   mv physionet.org/files/mimiciii/1.4/* .
   rm -rf physionet.org
   ```

### Verification
After downloading, run the verification script to check file integrity:
```bash
cd /e/Z5008_Readmission_Project
bash verify_mimiciii_files.sh
```

## 4. Important Rules
- **Do not unzip**: Keep all files as `.csv.gz`. The pipeline processes them in compressed format.
- **Do not share**: MIMIC-III data is strictly for credentialed users. **NEVER upload raw data to GitHub or public repositories.**
- **Verify Sizes**: Ensure large files like `CHARTEVENTS.csv.gz` (~4 GB) and `LABEVENTS.csv.gz` (~320 MB) are fully downloaded.
