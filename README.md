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

## Pre_Process_CheckInvalidData.py

This script validates vibration data stored in CSV files within a specified folder. It checks each file for:

* Missing or empty values
* NaN entries
* Invalid numeric data in X, Y, Z columns
* Incorrect column count
* Prints the exact row and column name, and provides a summary of total and invalid rows for each file.

Result when processing the data file in folder:
```
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
