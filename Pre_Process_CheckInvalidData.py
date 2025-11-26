
# -*- coding: utf-8 -*-# Nov 25 2025
"""
Purpose: Validate and analyze vibration CSV files in a folder.
Checks for empty, NaN, or invalid numeric data and reports row/column issues.
"""

import os
import csv
import math

folder_path = r"./vibration_data/20251125"  # Update folder path

# Process all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        print(f"\nProcessing file: {file_name}")

        invalid_rows = 0
        total_rows = 0

        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header
            for i, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                total_rows += 1
                if len(row) != 4:
                    print(f"Row {i}: Invalid column count -> {row}")
                    invalid_rows += 1
                    continue

                for col_idx, value in enumerate(row):
                    if value.strip() == "" or value.lower() == "nan":
                        print(f"Row {i}, Column {header[col_idx]}: Empty or NaN -> '{value}'")
                        invalid_rows += 1
                    else:
                        # Check numeric columns (X, Y, Z)
                        if col_idx > 0:  # Skip DATETIME
                            try:
                                num = float(value)
                                if math.isnan(num):
                                    print(f"Row {i}, Column {header[col_idx]}: NaN detected")
                                    invalid_rows += 1
                            except ValueError:
                                print(f"Row {i}, Column {header[col_idx]}: Invalid number -> '{value}'")
                                invalid_rows += 1

        print(f"Summary for {file_name}:")
        print(f"  Total rows: {total_rows}")
        print(f"  Invalid rows: {invalid_rows}")
