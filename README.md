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


