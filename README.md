# 🔎 Project FINDIT  
**Facilitating Intra-Departmental Navigation of Data and Information Transfer**

---

## 📌 Challenge Summary

Project FINDIT is a **data management initiative** for the Department of Psychology and Biobehavioral Science (PBS).  
The project develops tools called **"finders"** (or crawlers) that automatically scan directories, extract metadata, and perform data management or preprocessing tasks.  

---

## 🎯 Goals

- Build **basic finders** for:
  - Data inventory (what data we have and where it is stored)  
  - Metadata extraction  

- Extend to **advanced finders** for:
  - Automated preprocessing of data  
  - Domain-specific tasks (e.g., detecting EEG data and performing automated artifact correction)  

---

## 🏗️ Project History

- **Last Year’s Hackathon**:  
  Built an **inventory finder** that profiles data stored in a given directory.  

- **This Year’s Hackathon**:  
  Focus on a **participant-first finder**:  
  - Input: Subject ID  
  - Output: A report showing all available data for that participant (e.g., imaging, clinical, sleep tracking, questionnaires).  
  - Goal: Make it easy for researchers to quickly determine what data is available for any given research participant.  

---
## 🚀 Usage

### 📂 file_crawler

**file_crawler** is an R project that recursively scans directories to create an inventory of files.  
It captures file metadata (paths, names, sizes, modified times, and types) and, for SAS datasets (`.sas7bdat`), calculates the number of unique patient identifiers (MRNs).  

### 📂 first_findr

```
## 🚀 Future Directions

- Improve automation for large-scale data workflows  
- Expand finder functionality to support additional data types  
- Integrate into department-wide data management pipelines  

---
