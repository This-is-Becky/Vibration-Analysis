# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 15:31:00 2024

@author: beckylin
"""
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt 
import os
import numpy as np

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)

    # Convert numeric columns (X, Y, Z) to float, drop rows with invalid values
    for col in ["X", "Y", "Z"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["X", "Y", "Z"])

    df["Time"] = df["DATETIME"].apply(time_to_second)
    df["Duration"] = (df["Time"] - df["Time"].iloc[0]).dt.total_seconds() / 60
    return df

def time_to_second(time):
    str_val = str(time).zfill(9)
    hours = int(str_val[:2])
    minutes = int(str_val[2:4])
    seconds = int(str_val[4:6])
    milliseconds = int(str_val[6:])
    return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

def offset_data(df, columns):
    for col in columns:
        df[f"{col}_offset"] = df[col] - df[col].mean()
    return df

def plot_data(time, x, y, z, save_path):
    plt.figure(figsize=(10, 5))
    
    plt.plot(time, x, label="X data", color="#FF6347", zorder=3)
    plt.plot(time, y, label="Y data", color="#FFD700", zorder=2)
    plt.plot(time, z, label="Z data", color="#4169E1", zorder=1)
    
    overall_max = max(x.max(), y.max(), z.max())
    overall_min = min(x.min(), y.min(), z.min())
    
    plt.axhline(overall_max, linestyle="--", color="orange", label=f"Max: {overall_max:.2f}")
    plt.axhline(overall_min, linestyle="--", color="orange", label=f"Min: {overall_min:.2f}")
    
    plt.title("Overall acceleration over time")
    plt.xlabel("mins")
    plt.ylabel("m/s^2")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    # plt.show()

def plot_data_seperate(time, col, save_path):
    colors=["red", "blue", "green"]
    for col, color in zip(col, colors):
        plt.figure(figsize=(10, 5))
        plt.plot(time, col, label=f"{col.name[0]} data", color=color)
        
        max_value= col.max()
        min_value= col.min()
        plt.axhline(max_value, linestyle="--", color="orange", label=f"Max: {max_value:.2f}")
        plt.axhline(min_value, linestyle="--", color="orange", label=f"Min: {min_value:.2f}")
        plt.title(f"{col.name[0]} acceleration over time")
        plt.xlabel("mins")
        plt.ylabel("m/s^2")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        #Save each axis each plot
        save_path= f"{plot_path_sep}_{col.name}.png"
        plt.savefig(save_path)
        plt.close() 
        # plt.show()

def compute_rms(df, columns):
    """Compute overall RMS for each axis."""
    rms_values = {}
    for col in columns:
        rms_values[col] = np.sqrt(np.mean(df[col] ** 2))
    return rms_values


def plot_rms_bar(rms_values, save_path):
    """Plot RMS values as a bar chart."""
    plt.figure(figsize=(6, 4))
    axes = list(rms_values.keys())
    values = list(rms_values.values())
    colors = ["red", "blue", "green"]
    bars = plt.bar(axes, values, color=colors)    
    # Add value labels on top of each bar
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{value:.2f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.title("Overall RMS per Axis")
    plt.ylabel("RMS (m/s^2)")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


# Main Script
data_path = "./Data./20251125"
result_folder = "./result./20251125./raw plot"
os.makedirs(result_folder, exist_ok=True)


csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]

for file in csv_files:
    file_path = os.path.join(data_path, file)
    df = load_and_preprocess(file_path)
    df = offset_data(df, ["X", "Y", "Z"])

    #Save Combine XYZ plot 
    plot_path = os.path.join(result_folder, f"{os.path.splitext(file)[0]}_xyz_plot.png")
    plot_data(df["Duration"], df["X_offset"], 
          df["Y_offset"], df["Z_offset"], plot_path)
    
    #Save Sep XYZ plot 
    subfolder = os.path.join(result_folder, os.path.splitext(file)[0])
    os.makedirs(subfolder, exist_ok=True)
    plot_path_sep = os.path.join(subfolder, os.path.splitext(file)[0])
    plot_data_seperate(df["Duration"], [df["X_offset"], 
          df["Y_offset"], df["Z_offset"]], plot_path_sep)
    
    
    # Compute and plot RMS
    rms_values = compute_rms(df, ["X_offset", "Y_offset", "Z_offset"])
    rms_bar_path = os.path.join(subfolder, f"{os.path.splitext(file)[0]}_rms_bar.png")
    plot_rms_bar(rms_values, rms_bar_path)



print(f"Plots saved in: {result_folder}")



# plot_data(df["Duration"], df["X_offset"], 
#           df["Y_offset"], df["Z_offset"])

# # plot_data_seperate(df["Duration"], [df["X"], 
# #           df["Y"], df["Z"]])

# plot_data_seperate(df["Duration"], [df["X_offset"], 
#           df["Y_offset"], df["Z_offset"]])