import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import pyreadstat  # For reading SAS files
import openpyxl  # For reading Excel files
from multiprocessing import Pool, cpu_count

# Get data
start_path = "[DEFINE FILE PATH]"

# Get all files recursively
all_files = []
for root, dirs, files in os.walk(start_path):
    for file in files:
        all_files.append(os.path.join(root, file))

# Create inventory with modified time and file path information
file_inventory = []

for file in all_files:
    file_stats = os.stat(file)
    file_info = {
        'file_path': file,
        'mtime': datetime.fromtimestamp(file_stats.st_mtime),
        'size': file_stats.st_size
    }
    file_inventory.append(file_info)

file_inventory = pd.DataFrame(file_inventory)

# Create inventory with exact type of file
file_inventory_type = []

for file in all_files:
    file_type = Path(file).suffix.lstrip('.')
    file_inventory_type.append({'file_path': file, 'file_type': file_type})

file_inventory_type = pd.DataFrame(file_inventory_type)

# Identify if file is greater than or less than 1 GB
file_inventory['file_size'] = file_inventory['size'].apply(
    lambda x: "greater than 1 GB" if x > 100000000 else "less than 1GB"
)

# Define the MRN to search for
specific_mrn = "2357" #[ADD MRN INTEGER]  # Replace with the MRN you want to count

# Function to count MRN in columns that contain "MRN" in the header
def count_mrn_in_dataframe(df, mrn_to_count):
    """Count occurrences of MRN in columns that have 'MRN' in their name"""
    total_count = 0
    
    # Find columns that contain 'MRN' (case-insensitive)
    mrn_columns = [col for col in df.columns if 'mrn' in str(col).lower()]
    
    # Count occurrences in those columns
    for col in mrn_columns:
        # Try numeric comparison first
        try:
            # Convert MRN to number for comparison
            mrn_numeric = float(mrn_to_count) if '.' in str(mrn_to_count) else int(mrn_to_count)
            col_count = (df[col] == mrn_numeric).sum()
            total_count += col_count
        except (ValueError, TypeError):
            # If numeric comparison fails, fall back to string comparison
            col_count = (df[col].astype(str) == str(mrn_to_count)).sum()
            total_count += col_count
    
    return total_count

# Function to process each file
def process_file(args):
    file, mrn_to_count = args
    
    # Extract file extension
    file_type = Path(file).suffix.lstrip('.')
    
    try:
        # Check the file type and process accordingly
        if file_type in ['sas7bdat', 'sas']:
            file_test, meta = pyreadstat.read_sas7bdat(file)
            # Count occurrences of the specific MRN in columns with 'MRN' in header
            mrn_count = count_mrn_in_dataframe(file_test, mrn_to_count)
            return {'file': os.path.basename(file), 'mrn_count': mrn_count}
        
        elif file_type == 'xlsx':
            file_test = pd.read_excel(file)
            # Count occurrences of the specific MRN in columns with 'MRN' in header
            mrn_count = count_mrn_in_dataframe(file_test, mrn_to_count)
            return {'file': os.path.basename(file), 'mrn_count': mrn_count}
        
        elif file_type == 'csv':
            file_test = pd.read_csv(file)
            # Count occurrences of the specific MRN in columns with 'MRN' in header
            mrn_count = count_mrn_in_dataframe(file_test, mrn_to_count)
            return {'file': os.path.basename(file), 'mrn_count': mrn_count}
        
        else:
            # If not a recognized file type, return None for mrn_count
            return {'file': os.path.basename(file), 'mrn_count': None}
    
    except Exception as e:
        print(f"Error processing {file}: {str(e)}")
        return {'file': os.path.basename(file), 'mrn_count': None}

# Get the number of cores available for parallel processing
num_cores = cpu_count() - 1  # Use one less than the total number of cores

# Create arguments for parallel processing
file_args = [(file, specific_mrn) for file in all_files]

# Use Pool for parallel processing
if __name__ == '__main__':
    with Pool(num_cores) as pool:
        file_results = pool.map(process_file, file_args)

    # Combine the results into a single DataFrame
    file_mrn_counts = pd.DataFrame(file_results)

    # Append all information onto one single directory
    file_inventory_updated = file_inventory[['file_path', 'mtime', 'file_size']].copy()
    file_inventory_updated['file_type'] = file_inventory_type['file_type']
    file_inventory_updated['file_name'] = file_inventory_updated['file_path'].apply(os.path.basename)
    file_inventory_updated['folder_path'] = file_inventory_updated['file_path'].apply(os.path.dirname)
    file_inventory_updated['folder_name'] = file_inventory_updated['folder_path'].apply(os.path.basename)
    file_inventory_updated['mrn_count'] = file_mrn_counts['mrn_count']
    
    # Select final columns
    file_inventory_updated = file_inventory_updated[['folder_name', 'file_name', 'mrn_count', 
                                                      'mtime', 'file_type', 'file_size']]
    
    
    # ---------------------------
    # Save CSV
    # ---------------------------
    output_dir = ("[DEFINE FILE PATH]")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "participant_first_findr.csv")

    file_inventory_updated.to_csv(output_file, index=False)
    print(f"File saved to: {output_file}")

