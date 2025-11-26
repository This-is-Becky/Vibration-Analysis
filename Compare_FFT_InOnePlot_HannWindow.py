## Removed DC offset before FFT
## Hanning Window (Noted:reduces amplitude slightly (because of tapering).)
##Produces a smoother spectrum with reduced spectral leakage.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FFT_CHANNEL = "Z_offset"
FFT_MIN = 1024
data_folder = "./Data./20251125"
result_folder = "./result./20251125"
os.makedirs(result_folder, exist_ok=True)

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    if df.empty:
        return df
        
    # Convert numeric columns (X, Y, Z) to float, drop rows with invalid values
    for col in ["X", "Y", "Z"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["X", "Y", "Z"])


    df["Time"] = df["DATETIME"].apply(lambda x: pd.Timedelta(
        hours=int(str(x).zfill(9)[:2]),
        minutes=int(str(x).zfill(9)[2:4]),
        seconds=int(str(x).zfill(9)[4:6]),
        milliseconds=int(str(x).zfill(9)[6:])
    ))
    df["Duration"] = (df["Time"] - df["Time"].iloc[0]).dt.total_seconds()
    for col in ["X", "Y", "Z"]:
        df[f"{col}_offset"] = df[col] - df[col].mean()
    return df

def detect_sampling_rate(df):
    duration_sec = (df["Time"].iloc[-1] - df["Time"].iloc[0]).total_seconds()
    return len(df) / duration_sec

def compute_fft(signal, fs):
    L = len(signal)
    if L < FFT_MIN:
        return None, None
    #Find the nearest bit of power of 2 for the Total data Length
    # L_pow2 = 1 << (L.bit_length() - 1)

    #Remove DC offset
    # sig = signal[-L_pow2:] - np.mean(signal[-L_pow2:])
    sig = signal - np.mean(signal)
    #Apply Hanning Window
    win = np.hanning(L)
    #FFT
    Y = np.fft.rfft(sig * win)
    freqs = np.fft.rfftfreq(L, d=1.0/fs)
    
    # Normalize amplitude, abs to keep absoulte value since we cares about how strong each frequency is, not its phase.
    # (L / 2.0)for single-sided spectrum(positive frequencies)
    mag = np.abs(Y) / (L / 2.0)
    return freqs, mag

# Combined FFT plot
plt.figure(figsize=(10, 6))

for file in os.listdir(data_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(data_folder, file)
        df = load_and_preprocess(file_path)
        if df.empty:
            continue
        fs = detect_sampling_rate(df)
        freqs, mag = compute_fft(df[FFT_CHANNEL].values, fs)
        if freqs is not None:
            print(f"File:{file}; Sampling rate:(fs={round(fs,2)} Hz)")
            # Find peak frequency and amplitude
            peak_idx = np.argmax(mag)
            peak_freq = freqs[peak_idx]
            peak_amp = mag[peak_idx]

            # Plot FFT curve
            line, = plt.plot(freqs, mag, label=f"{file} (Peak: {peak_freq:.2f} Hz)")
            color = line.get_color()

            # Add dot at peak
            plt.scatter(peak_freq, peak_amp, color=color, zorder=5)


plt.title(f"FFT Comparison of {FFT_CHANNEL} Across Files")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude(m/s^2)")
plt.xlim(0, 500)  # Adjust based on your interest range
plt.grid(True)
plt.legend(fontsize=8)
# plt.tight_layout()
# plt.show()

# Save Comparing freq 
fft_path = os.path.join(result_folder, f"{FFT_CHANNEL}_freq_comparison_chart.png")
plt.tight_layout()
plt.savefig(fft_path)
plt.close()

print(f"Results saved in: {result_folder}")