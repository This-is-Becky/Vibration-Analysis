# Vibration-Analysis
Included various analysis approach for vibration, from data structure, sampling rate to wave plot and FFT frequency.

## Cal_SamplingRate_InDiffTimeStamp.py
This Python script analyzes vibration data stored in a CSV file to calculate the sampling rate. It reads timestamps from the first column, converts them into datetime objects, and computes:

* Sampling rate for specific seconds (1st, 2nd, 6th, and 20th).
* Average sampling rate across the entire dataset.
* Result(Using PC_fan.csv as example):
```
Sampling rate in 1st second: 460 points
Sampling rate in 2nd second: 461 points
Sampling rate in 6th second: 463 points
Sampling rate in 20nd second: 461 points
Average sampling rate: 460.83 Hz
```

Result in(300.csv as example):
```
Sampling rate in 1st second: 917 points
Sampling rate in 2nd second: 918 points
Sampling rate in 6th second: 917 points
Sampling rate in 20nd second: 917 points
Average sampling rate: 916.88 Hz
```

## Pre_Process_CheckInvalidData.py

This script validates vibration data stored in CSV files within a specified folder. It checks each file for:

* Missing or empty values
* NaN entries
* Invalid numeric data in X, Y, Z columns
* Incorrect column count
* Prints the exact row and column name, and provides a summary of total and invalid rows for each file.

Result when processing the data file in folder:
```
Processing file: 300.csv
Summary for 300.csv:
  Total rows: 31220
  Invalid rows: 0

Processing file: Data_with_NaN_Column.csv
Row 2, Column X: Empty or NaN -> ' '
Summary for Data_with_NaN_Column.csv:
  Total rows: 23111
  Invalid rows: 1

Processing file: PC_fan.csv
Summary for PC_fan.csv:
  Total rows: 34493
  Invalid rows: 0

Processing file: Rpi_fan.csv
Summary for Rpi_fan.csv:
  Total rows: 23111
  Invalid rows: 0
```

## Compare_FFT_InOnePlot_HannWindow.py
The script process the data to visualized the FFT frequency of each file.

* Cleans invalid rows of each files, computes the Fast Fourier Transform (FFT) for the Z-axis signal(which could be adjusted in different axis).
* Applies offset removal and a Hanning window Function to minimize spectral leakage, producing a smoother frequency spectrum.
* Plots FFT results for all files on a single chart, highlights peak frequencies, and saves the comparison plot in target specify folder.

Result:

<img width="500" height="300" alt="Z_offset_freq_comparison_chart" src="https://github.com/user-attachments/assets/72253bd2-3d1e-4d87-a088-a3c042f3a0e3" />

## Plot_XYZ_RMS_Separately.py

This Python script processes the data from CSV files, and compute the rms values, and plot the waveform for better visualization.

* Cleans invalid rows.
* Analyses on acceleration data (X, Y, Z axes), and plot the waveform, for XYZ combination, and separate XYZ plot as well.
* Removes offset, which means the data will centralize by 0(0 as the baseline).
* Computes RMS values, and generates visualizations RMS bar charts for each axis for each file. 
* All results are saved in target folders as define.
  
## Plot_RMS_Comparison.py

The script automate process multiple CSV data files in Data folder, and compute the RMS.
* Pre-process the data>> Removes offset, makes data centralize by 0
* Compute RMS values for each file, and plot the results in a bar chart for comparison.
* Generates a summary csv. report for further analysis and visualization.
   
## Result can be found in the "result" folder
