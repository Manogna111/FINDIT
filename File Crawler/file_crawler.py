"""
Title: file_crawler
Author: Manogna
Date: 2024-09-04
Output: HTML-like report
"""

# ---------------------------
# Load libraries
# ---------------------------
import os
import pandas as pd
import pyreadstat
import multiprocessing as mp
from datetime import datetime
import docx
import traceback


# Define the folder to crawl
# ---------------------------
start_path = "C:/Users/manog/Downloads/BIOHACKATHON/2025/Gibney_Kyla"  

# ---------------------------
# Function to process each file (parallelized)
# ---------------------------
def process_file(file):
    file_type = os.path.splitext(file)[1].lower().replace(".", "")
    
    try:
        # Handle SAS7BDAT files
        if file_type == "sas7bdat":
            df, meta = pyreadstat.read_sas7bdat(file)
            unique_mrn_count = df.iloc[:, 0].nunique()
        #Handle SAS files
        elif file_type == "sas":
            unique_mrn_count = "NA"

        # Handle Excel files
        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(file)
            unique_mrn_count = df.iloc[:, 0].nunique() if not df.empty else 0

        # Handle CSV files
        elif file_type == "csv":
            df = pd.read_csv(file)
            unique_mrn_count = df.iloc[:, 0].nunique() if not df.empty else 0

        # Handle text files
        elif file_type in ["txt", "log"]:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            unique_mrn_count = len(set(lines))  # crude: count unique lines

        # Skip Word documents
        elif file_type == "docx":
            unique_mrn_count = "NA"

        # Unsupported file type
        else:
            unique_mrn_count = "NA"

        return {"file": os.path.basename(file), "unique_mrn_count": unique_mrn_count}

    except Exception as e:
        print(f"Error processing {file}: {e}")
        traceback.print_exc()
        return {"file": os.path.basename(file), "unique_mrn_count": None}


if __name__ == "__main__":
    # ---------------------------
    # Get all files in the folder (recursive)
    # ---------------------------
    all_files = []
    for root, dirs, files in os.walk(start_path):
        for f in files:
            all_files.append(os.path.join(root, f))

    # ---------------------------
    # Create inventory w/ modified time and file path
    # ---------------------------
    file_inventory = pd.DataFrame()
    for file in all_files:
        try:
            stat_info = os.stat(file)
            file_info = {
                "size": stat_info.st_size,
                "mtime": datetime.fromtimestamp(stat_info.st_mtime),
                "file_path": file,
            }
            file_inventory = pd.concat([file_inventory, pd.DataFrame([file_info])], ignore_index=True)
        except Exception as e:
            print(f"Error reading file {file}: {e}")

    # ---------------------------
    # Create inventory w/ exact type of file
    # ---------------------------
    file_inventory_type = pd.DataFrame()
    for file in all_files:
        file_ext = os.path.splitext(file)[1].replace(".", "")
        temp_df = pd.DataFrame([{"file_path": file, "file_type": file_ext}])
        file_inventory_type = pd.concat([file_inventory_type, temp_df], ignore_index=True)

    # ---------------------------
    # Identify if file is greater than or less than 1 GB
    # ---------------------------
    file_inventory["file_size"] = file_inventory["size"].apply(
        lambda x: "greater than 1 GB" if x > 1_000_000_000 else "less than 1GB"
    )

    # ---------------------------
    # Parallel processing
    # ---------------------------
    num_cores = max(1, mp.cpu_count() - 1)
    with mp.Pool(num_cores) as pool:
        file_results = pool.map(process_file, all_files)

    file_unique_mrn = pd.DataFrame(file_results)

    # ---------------------------
    # Append all information
    # ---------------------------
    file_inventory_updated = (
        file_inventory[["file_path", "mtime", "file_size"]]
        .merge(file_inventory_type, on="file_path", how="left")
        .assign(
            file_name=lambda df: df["file_path"].apply(os.path.basename),
            folder_path=lambda df: df["file_path"].apply(os.path.dirname),
        )
    )

    file_inventory_updated["folder_name"] = file_inventory_updated["folder_path"].apply(os.path.basename)

    # Merge unique_mrn_count
    file_inventory_updated = file_inventory_updated.merge(
        file_unique_mrn, left_on="file_name", right_on="file", how="left"
    )

    file_inventory_updated = file_inventory_updated[
        ["folder_name", "file_name", "unique_mrn_count", "mtime", "file_type", "file_size"]
    ]

    # ---------------------------
    # Save CSV
    # ---------------------------
    output_dir = ("C:/Users/manog/Downloads/BIOHACKATHON/2025/data/processed_data")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "file_inventory_updated.csv")

    file_inventory_updated["unique_mrn_count"] = pd.to_numeric(file_inventory_updated["unique_mrn_count"], errors="coerce")
    file_inventory_updated["mtime"] = file_inventory_updated["mtime"].astype(str)
    file_inventory_updated["file_size"] = file_inventory_updated["file_size"].astype(str)

    file_inventory_updated.to_csv(output_file, index=False)
    print(f"File saved to: {output_file}")
