import pandas as pd
from datetime import datetime

# Path to your CSV file
data_file = "./vibration_data./20251125./202511251457.csv"  # Update path if needed

# Read CSV into DataFrame
df = pd.read_csv(data_file)

timestamps = []

# Convert HHMMSSmmm (e.g., 133845041) to datetime
for dt_str in df.iloc[:, 0]:  # Assuming first column is time
    try:
        ts = datetime.strptime(str(dt_str).zfill(9), "%H%M%S%f")
        timestamps.append(ts)
    except ValueError:
        continue

timestamps.sort()

if timestamps:
    start_time = timestamps[0]

    # Sampling rate for 1st second
    sampling_rate_1st_sec = sum(1 for t in timestamps if 0 <= (t - start_time).total_seconds() < 1)

    # Sampling rate for 2nd second
    sampling_rate_2nd_sec = sum(1 for t in timestamps if 1 <= (t - start_time).total_seconds() < 2)


    # Sampling rate for 6th second
    sampling_rate_6th_sec = sum(1 for t in timestamps if 5 <= (t - start_time).total_seconds() < 6)

    # Sampling rate for 10th second
    sampling_rate_20th_sec = sum(1 for t in timestamps if 19 <= (t - start_time).total_seconds() < 20)

    # Average sampling rate
    diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
    avg_interval = sum(diffs)/len(diffs) if diffs else 0
    avg_sampling_rate = 1/avg_interval if avg_interval > 0 else 0

    print(f"Sampling rate in 1st second: {sampling_rate_1st_sec} points")
    print(f"Sampling rate in 2nd second: {sampling_rate_2nd_sec} points")
    print(f"Sampling rate in 6th second: {sampling_rate_6th_sec} points")
    print(f"Sampling rate in 20nd second: {sampling_rate_20th_sec} points")
    # print(f"Data points in first 5 seconds: {five_second_count}")
    # print(f"Sampling rate in 6th second: {sampling_rate_6th_sec} points")
    print(f"Average sampling rate: {avg_sampling_rate:.2f} Hz")
else:
    print("No valid timestamps found.")