# 📂 file_crawler

**file_crawler** is an R project that recursively scans directories to create an inventory of files.  
It captures file metadata (paths, names, sizes, modified times, and types) and, for SAS datasets (`.sas7bdat`), calculates the number of unique patient identifiers (MRNs).  

The script outputs a structured CSV file, making it easy to analyze and audit file systems.

---

## ✨ Features

- 🔍 Recursively scans all files in a directory  
- 📝 Collects metadata:  
  - File path & name  
  - Folder path & name  
  - File type (extension)  
  - Last modified time (`mtime`)  
  - File size classification (less than or greater than 1 GB)  
- 📊 Extracts **unique MRN counts** from `.sas7bdat` files (first column assumed to be `mrn`)  
- ⚡ Supports **parallel processing** for faster file handling  
- 📁 Saves results to `../data/processed_data/file_inventory_updated.csv`  

---

## 📦 Requirements

Install the following R packages:

```r
install.packages(c(
  "tidyverse",
  "haven",
  "tools",
  "data.table",
  "parallel",
  "readr"
))
