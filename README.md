## Overview

This script is designed for deduplication of Excel-based trade data. It processes data files from various countries, identifying and removing duplicate records to create clean datasets. The script traverses a directory of country-specific subfolders, reads Excel files containing import and export data, and deduplicates this data using the pandas_dedupe library.

## Functionality

1. **Directory Traversal**: The `os_path_walk` function scans a given directory, identifying subfolders representing different countries and listing all Excel files within these subfolders.

2. **DataFrame Creation**: The `get_dataframe` function reads the identified Excel files, loading specific sheets based on the type (import/export). It cleans the data by stripping whitespace from column names and filling empty cells with 'Unknown'.

3. **Deduplication**: The `learning_fn` function applies the pandas_dedupe library to deduplicate the data. It uses specified field properties to train the deduplication model, ensuring a 70% threshold confidence level and processing 80% of the data for training.

4. **Processing Workflow**: The script iterates over each country and data type (import/export), reads the data files, deduplicates the data based on specified fields (e.g., Shipper, Consignee), and saves the cleaned data to new Excel files.

## Usage

1. **Setup**: Ensure the `target_data`, `config_base`, and `result_base` directories are correctly set in the `consts.py` file.
2. **Run**: Execute the script to process all available country-specific data files. The script will skip files that have already been processed.
3. **Output**: Cleaned and deduplicated data files are saved in the `result_base` directory, with filenames indicating the country and data type (e.g., `China_Import.xlsx`).

## Example

For China, the script will:
- Traverse the directory to find all Excel files.
- Read import and export data files.
- Deduplicate records based on fields like Shipper and Consignee.
- Save the cleaned data to `result_base/China_Import.xlsx` and `result_base/China_Export.xlsx`.

This automated workflow ensures consistent and accurate deduplication of trade data, facilitating subsequent data analysis tasks.
