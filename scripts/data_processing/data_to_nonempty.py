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
# GENERATES: nonempty_class_<data name>.csv
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


def extract_nonzero_class_rows(folder_path, file_name):
    """
    Read the CSV file from the given folder and extract rows where the last column (class) is not 0.
    Save the extracted rows into a new CSV file in the same folder.

    Parameters:
    - folder_path: str, path to the folder containing the CSV file
    - file_name: str, name of the CSV file to process
    """
    # Construct the full path to the CSV file
    csv_path = os.path.join(folder_path, file_name)

    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Get the name of the last column
    class_column = df.columns[-1]

    # Extract rows where the class is not 0
    df_nonzero_class = df[df[class_column] != 0]

    # Save the extracted DataFrame back to CSV
    new_file_name = f"nonempty_class_{file_name}"
    modified_csv_path = os.path.join(folder_path, new_file_name)
    df_nonzero_class.to_csv(modified_csv_path, index=False)
    print(f"Extracted rows with nonzero class from {file_name} and saved as {modified_csv_path}")

# Check if the folder exists

if os.path.exists(folder_path):
    # Modify 'train.csv' and 'test.csv'
    for file_name in tqdm(files):
        extract_nonzero_class_rows(folder_path, file_name)
else:
    print("The specified folder does not exist.")