# Vibration-Analysis
Included various analysis approach for vibration, from data structure, sampling rate to wave plot and FFT frequency.

## Cal_SamplingRate_InDiffTimeStamp.py
This Python script analyzes vibration data stored in a CSV file to calculate the sampling rate. It reads timestamps from the first column, converts them into datetime objects, and computes:

* Sampling rate for specific seconds (1st, 2nd, 6th, and 20th).
* Average sampling rate across the entire dataset.
* Result:
  <img width="250" height="60" alt="image" src="https://github.com/user-attachments/assets/5c3ce1ac-2e82-46fd-aac4-44f4908fee7c" />
