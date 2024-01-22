# This script is designed to process CSV files by extracting rows where the last column 
# (assumed to be the class) is not zero. This functionality is particularly useful for 
# datasets where classes are numerically labeled and there is a need to focus on non-zero 
# classes, such as in certain types of classification tasks or data analyses.
# The script operates by reading an existing CSV file from a specified folder, 
# filtering out rows where the class is not 0, and then saving the extracted rows 
# into a new file in the same folder. This approach is useful for preprocessing datasets 
# where classes of interest are represented by non-zero values.
# By saving the extracted data in a new file, the script ensures the original data remains 
# unaltered, maintaining data integrity. This feature is important when working with raw 
# datasets that may need to be accessed in their original form for other analyses.
# The script is flexible and can be applied to various CSV files within a directory, 
# allowing for batch processing of datasets, as demonstrated with 'train.csv' and 'test.csv'.
#
# GENERATES: nonzero_class_<data name>.csv
#

import pandas as pd
import os
from tqdm import tqdm
import argparse


# Specify the folder path where 'train.csv' and 'test.csv' are located
files = ['train.csv', 'test.csv']

# Setup argparse for command line arguments
parser = argparse.ArgumentParser(description='Dataset Analysis')
parser.add_argument('dataset_name', type=str, help='Enter the X_dataset_name')
parser.add_argument('fold_number', type=int, help='Enter the fold number')
args = parser.parse_args()

folder_path = f"../../data/{args.dataset_name}/fold_{args.fold_number}"

def extract_nonzero_class_groups(folder_path, file_name):
    """
    Read the CSV file from the given folder and keep groups of rows where the last row 
    of each group (based on the first column as the ID) has a non-zero value in the last column.
    Save the resulting DataFrame back to the same folder.

    Parameters:
    - folder_path: str, path to the folder containing the CSV file
    - file_name: str, name of the CSV file to process
    """
    # Construct the full path to the CSV file
    csv_path = os.path.join(folder_path, file_name)

    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Get the name of the first column (ID) and the last column (class)
    id_column = df.columns[0]
    class_column = df.columns[-1]

    # Group by the ID column and filter groups
    grouped = df.groupby(id_column)
    filtered_groups = [group for _, group in grouped if group[class_column].iloc[-1] != 0]

    # Concatenate the filtered groups into a new DataFrame
    filtered_df = pd.concat(filtered_groups, ignore_index=True)

    # Save the filtered DataFrame back to CSV
    new_file_name = f"filtered_{file_name}"
    modified_csv_path = os.path.join(folder_path, new_file_name)
    filtered_df.to_csv(modified_csv_path, index=False)
    print(f"Extracted rows with nonzero class in the last row of groups from {file_name} and saved as {modified_csv_path}")

# Check if the folder exists

if os.path.exists(folder_path):
    # Modify 'train.csv' and 'test.csv'
    for file_name in tqdm(files):
        extract_nonzero_class_groups(folder_path, file_name)
else:
    print("The specified folder does not exist.")