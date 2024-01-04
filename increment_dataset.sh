#!/bin/bash

# Define the source and destination directories
source_dir="./air_qualliry_regressor_prepocess/out"
data_dir="./data"
models_single_dir="./models/single"
models_dual_dir="./models/dual"

# Check if the source directory exists and has folders in it
if [ -d "$source_dir" ] && [ "$(ls -A $source_dir)" ]; then
    # Prompt the user for the dataset name
    read -p "Enter the dataset name: " dataset_name

    # Find the highest existing X value
    last_x=$(ls $data_dir | grep -E "^([0-9]+)_${dataset_name}$" | sort -r | head -n 1 | cut -d'_' -f1)

    # If no existing folders, start with 1; otherwise, increment by 1
    if [ -z "$last_x" ]; then
        x=1
    else
        x=$((last_x + 1))
    fi

    # Create the new dataset directory
    new_dataset_dir="${data_dir}/${x}_${dataset_name}"
    mkdir -p "$new_dataset_dir"

    # Move all folders from the source to the new dataset directory
    mv ${source_dir}/* "${new_dataset_dir}/"

    # Create corresponding folders in models/single and models/dual
    mkdir -p "${models_single_dir}/${x}_${dataset_name}"
    mkdir -p "${models_dual_dir}/${x}_${dataset_name}"

    echo "Folders moved to ${new_dataset_dir} and corresponding model directories created."

    echo "Summarizing dataset..."
    python analize_dataset.py ${x}_${dataset_name} 1

    mv charts data/${x}_${dataset_name}
    echo "Done!"

else
    echo "No folders found in ${source_dir}."
fi
