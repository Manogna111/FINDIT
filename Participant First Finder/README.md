# 📂 participant_first_findr

An R-based workflow for **crawling directories based on patient MRNs** across multiple file types (CSV, Excel, SAS).  
Optimized for large datasets with **parallel processing**.  

---

## ✨ Features
- 🔍 Recursively crawls a directory to **list all files**  
- 🗂 Builds a **file inventory** with:
  - File path & name  
  - File type (extension)  
  - Last modified time (`mtime`)  
  - File size (`<1 GB` or `>1 GB`)  
- 🔢 Searches files for a **specific MRN** (e.g., `"2759"`) across:
  - `.sas7bdat` / `.sas` (SAS files)  
  - `.csv`  
  - `.xlsx`  
- ⚡ Speeds up file scanning using **parallel processing**  
- 📑 Outputs a **consolidated dataset** with metadata + MRN counts  

---

## 🛠 Requirements

Install the following R packages before running:

```r
install.packages(c("tidyverse", "data.table", "parallel", "readxl", "haven", "tools"))
