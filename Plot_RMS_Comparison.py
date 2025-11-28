# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 11:49:41 2025

@author: beckylin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 15:08:37 2025
@author: beckylin
"""

import os
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Paths
data_folder = "./Data./20251125"  # Change to your actual folder
result_folder = "./result./20251125"
os.makedirs(result_folder, exist_ok=True)

def load_and_preprocess(file_path):
    clean_rows = []
    # Step 1: Read and filter rows
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader, start=1):
            if len(row) == 4:  # Keep only rows with 4 columns
                clean_rows.append(row)
            else:
                print(f"Dropped line {i} in {os.path.basename(file_path)}: {row}")

    # Step 2: Convert to DataFrame
    df = pd.DataFrame(clean_rows, columns=["DATETIME", "X", "Y", "Z"])

    # Step 3: Convert numeric columns
    for col in ["X", "Y", "Z"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with NaN after conversion
    df.dropna(subset=["X", "Y", "Z"], inplace=True)

    # Step 4: Compute time and offsets
    df["Time"] = df["DATETIME"].apply(lambda x: pd.Timedelta(hours=int(str(x).zfill(9)[:2]),
                                                             minutes=int(str(x).zfill(9)[2:4]),
                                                             seconds=int(str(x).zfill(9)[4:6]),
                                                             milliseconds=int(str(x).zfill(9)[6:])))
    df["Duration"] = (df["Time"] - df["Time"].iloc[0]).dt.total_seconds() / 60

    for col in ["X", "Y", "Z"]:
        df[f"{col}_offset"] = df[col] - df[col].mean()

    df["ins_rms"] = np.sqrt((df["X_offset"]**2 + df["Y_offset"]**2 + df["Z_offset"]**2) / 3)
    return df

def calculate_overall_rms(df):
    return np.sqrt(np.mean(df["ins_rms"]**2))

def show_bar_chart(labels, rms_values, save_path):
    palette = sns.color_palette("Set2", len(rms_values))
    plt.figure(figsize=(6, 5))
    bars = plt.bar(labels, rms_values, color=palette)
    plt.title('RMS Values')
    plt.xlabel('Measurement Point')
    plt.ylabel('RMS Value')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 3), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    plt.close()

# Main Script
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
overall_rms_values = []
labels = []

for file in csv_files:
    file_path = os.path.join(data_folder, file)
    df = load_and_preprocess(file_path)
    if not df.empty:
        rms = calculate_overall_rms(df)
        overall_rms_values.append(rms)
        labels.append(os.path.splitext(file)[0])
    else:
        print(f"No valid data in {file}")

# Save RMS summary
summary_df = pd.DataFrame({"File": labels, "Overall_RMS": overall_rms_values})
summary_path = os.path.join(result_folder, "rms_summary.csv")
summary_df.to_csv(summary_path, index=False)

# Save bar chart
chart_path = os.path.join(result_folder, "rms_bar_chart.png")
show_bar_chart(labels, overall_rms_values, chart_path)

print(f"Processed {len(csv_files)} files.")
print(f"Results saved in: {result_folder}")