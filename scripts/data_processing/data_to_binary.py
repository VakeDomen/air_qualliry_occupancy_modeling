# This script is designed to read CSV files and convert the last column into a binary 
# format where non-zero values are set to 1 and zero values remain 0.
# The primary purpose is to prepare datasets for analyses that require binary variables, 
# such as logistic regression or other binary classification algorithms.
# The script operates by reading an existing CSV file from a specified folder, 
# modifying the last column to be binary, and then saving the modified version back to 
# the same folder with a new name to preserve the original data.
# It's especially useful for preprocessing large datasets efficiently and ensures data 
# integrity by not overwriting original files.
# The script is flexible and can be used on multiple files within a directory, as 
# demonstrated with 'train.csv' and 'test.csv'.
#
# GENERATES: binary_class_<data name>.csv
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

def to_binary(num):
    if num > 0:
        return 1
    return 0

def modify_csv_to_binary(folder_path, file_name):
    """
    Read the CSV file from the given folder and modify the last column to be binary.
    Save the modified CSV back to the same folder.

    Parameters:
    - folder_path: str, path to the folder containing the CSV file
    - file_name: str, name of the CSV file to modify
    """
    # Construct the full path to the CSV file
    csv_path = os.path.join(folder_path, file_name)

    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Get the name of the last column
    last_column = df.columns[-1]

    # Modify the last column to be binary
    df[last_column] = df[last_column].map(to_binary)

    # Save the modified DataFrame back to CSV
    modified_csv_path = os.path.join(folder_path, f"binary_class_{file_name}")
    df.to_csv(modified_csv_path, index=False)
    print(f"Modified {file_name} and saved as {modified_csv_path}")


# Check if the folder exists

if os.path.exists(folder_path):
    # Modify 'train.csv' and 'test.csv'
    for file_name in tqdm(files):
        modify_csv_to_binary(folder_path, file_name)
else:
    print("The specified folder does not exist.")