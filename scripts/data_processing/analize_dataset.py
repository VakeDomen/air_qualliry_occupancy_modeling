import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os
import numpy as np
from tqdm import tqdm

# Additional functions for enhanced analysis
def analyze_missing_values(data, column, summary):
    missing_count = data[column].isnull().sum()
    summary.write(f'\n### Missing Values in {column}: {missing_count}\n')

def analyze_correlation(data, summary):
    plt.figure(figsize=(12, 10))
    sns.heatmap(data.corr(), annot=True, fmt=".2f")
    plt.title('Feature Correlation Matrix')
    corr_chart_path = './charts/correlation_matrix.png'
    plt.savefig(corr_chart_path)
    plt.close()
    summary.write(f"![Correlation Matrix]({corr_chart_path})\n")

# Existing function modified to include missing value analysis
def analyze_and_plot(data, column, summary, is_target=False):
    summary.write(f"\n## Analysis for column: {column}\n")
    desc = data[column].describe()
    summary.write(desc.to_markdown() + "\n")
    
    # Missing Values Analysis
    analyze_missing_values(data, column, summary)
    
    # Distribution Plot
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column].dropna(), kde=True)  # Drop NA for plotting
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    chart_path = f'./charts/{column}_distribution.png'
    plt.savefig(chart_path)
    plt.close()
    summary.write(f"![Distribution of {column}]({chart_path})\n")

    # Boxplot for target column
    if is_target:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=data[column])
        plt.title(f'Boxplot of {column}')
        boxplot_path = f'./charts/{column}_boxplot.png'
        plt.savefig(boxplot_path)
        plt.close()
        summary.write(f"![Boxplot of {column}]({boxplot_path})\n")

def analyze_dataset(dataset_name, fold_number):
    # Define the paths to the train and test CSV files
    base_dir = f"./data/{dataset_name}/fold_{fold_number}"
    train_path = os.path.join(base_dir, 'train.csv')
    test_path = os.path.join(base_dir, 'test.csv')

    # Check if the files exist
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        print("Train or test file not found.")
        return

    # Read the datasets
    print("Reading CSV files...")
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)

    # Create a directory to save charts
    if not os.path.exists('./charts'):
        os.makedirs('./charts')

    # Open a README.md file in write mode
    with open('./charts/README.md', 'w') as summary:
        summary.write(f"# Dataset Analysis for {dataset_name} - Fold {fold_number}\n")

        # Analyze each column of the train data
        for column in tqdm(train_data.columns[:-1]):  # Exclude the last column for now
            analyze_and_plot(train_data, column, summary)

         # Correlation Analysis
        summary.write("\n## Correlation Analysis\n")
        analyze_correlation(train_data, summary)


        # In-depth analysis for the last column (target variable)
        target_column = train_data.columns[-1]
        summary.write("\n## Performing in-depth analysis for the target variable...\n")
        analyze_and_plot(train_data, target_column, summary, is_target=True)

# Setup argparse for command line arguments
parser = argparse.ArgumentParser(description='Dataset Analysis')
parser.add_argument('dataset_name', type=str, help='Enter the X_dataset_name')
parser.add_argument('fold_number', type=int, help='Enter the fold number')
args = parser.parse_args()

print("Analizing")

analyze_dataset(args.dataset_name, args.fold_number)
