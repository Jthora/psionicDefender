import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave
import csv
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
import argparse
import os

# Constants (can be overridden by CLI)
DEFAULT_SAMPLING_RATE = 44100
FFT_WINDOW_SIZE = 1024
CHANNELS = 1

def analyze_file(file_path):
    """Analyze a .wav file for frequency components."""
    try:
        with wave.open(file_path, 'rb') as wf:
            if wf.getnchannels() > 1:
                print("Warning: File is not mono. Only the first channel will be processed.")
            frames = wf.readframes(wf.getnframes())
            signal = np.frombuffer(frames, dtype=np.int16)
            sampling_rate = wf.getframerate()

        frequencies, spectrum = perform_fft(signal, sampling_rate)
        save_results(frequencies, spectrum, "file_analysis_results.csv")
        visualize(signal, frequencies, spectrum, sampling_rate, "File Analysis")
    except Exception as e:
        print(f"Error analyzing file: {e}")

def analyze_real_time():
    """Analyze real-time audio input for frequency components."""
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=DEFAULT_SAMPLING_RATE, input=True, frames_per_buffer=FFT_WINDOW_SIZE)

        print("Recording... Press Ctrl+C to stop.")
        plt.ion()
        fig, ax = plt.subplots()
        while True:
            data = np.frombuffer(stream.read(FFT_WINDOW_SIZE, exception_on_overflow=False), dtype=np.int16)
            frequencies, spectrum = perform_fft(data, DEFAULT_SAMPLING_RATE)
            ax.clear()
            ax.plot(frequencies, spectrum)
            ax.set_title("Real-Time Frequency Spectrum")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Amplitude")
            ax.set_xlim(0, DEFAULT_SAMPLING_RATE // 2)
            plt.pause(0.01)
    except KeyboardInterrupt:
        print("\nStopping real-time analysis.")
    except Exception as e:
        print(f"Error in real-time analysis: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def perform_fft(signal, sampling_rate):
    """Perform FFT and calculate frequency spectrum."""
    fft_result = fft(signal)
    frequencies = fftfreq(len(fft_result), d=1/sampling_rate)
    spectrum = np.abs(fft_result)
    return frequencies[:len(frequencies)//2], spectrum[:len(spectrum)//2]

def save_results(frequencies, spectrum, file_name):
    """Save frequency analysis results to a .csv file."""
    try:
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Frequency (Hz)", "Amplitude"])
            for freq, amp in zip(frequencies, spectrum):
                writer.writerow([freq, amp])
        print(f"Results saved to {file_name}")
    except Exception as e:
        print(f"Error saving results: {e}")

def visualize(signal, frequencies, spectrum, sampling_rate, title="Frequency Analysis"):
    """Visualize time-domain and frequency-domain signals."""
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(np.arange(len(signal)) / sampling_rate, signal)
    plt.title("Time-Domain Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.subplot(2, 1, 2)
    plt.semilogx(frequencies, spectrum)
    plt.title(f"{title}: Frequency-Domain Signal")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Frequency Analysis Script")
    parser.add_argument("--file", type=str, help="Path to the .wav file for analysis")
    parser.add_argument("--real_time", action="store_true", help="Enable real-time analysis")
    parser.add_argument("--sampling_rate", type=int, default=DEFAULT_SAMPLING_RATE, help="Sampling rate (default: 44100 Hz)")
    parser.add_argument("--fft_size", type=int, default=FFT_WINDOW_SIZE, help="FFT window size (default: 1024)")
    args = parser.parse_args()

    # Update parameters based on user input
    DEFAULT_SAMPLING_RATE = args.sampling_rate
    FFT_WINDOW_SIZE = args.fft_size

    if args.file:
        if not os.path.exists(args.file):
            print(f"File {args.file} does not exist.")
        else:
            analyze_file(args.file)
    elif args.real_time:
        analyze_real_time()
    else:
        print("Please specify either --file or --real_time")