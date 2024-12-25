import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from scipy.signal import butter, lfilter
import argparse
import csv
import time

# Constants
DEFAULT_SAMPLING_RATE = 44100
BUFFER_SIZE = 1024
FILTER_ORDER = 4
LOG_FILE = "logs/cancellation_log.csv"

def band_stop_filter(data, lowcut, highcut, sampling_rate, order=FILTER_ORDER):
    """Apply a band-stop filter to the input signal."""
    nyquist = 0.5 * sampling_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='bandstop')
    return lfilter(b, a, data)

def process_audio_stream(target_frequency, bandwidth, sampling_rate):
    """Real-time noise cancellation for the target frequency."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sampling_rate, input=True, frames_per_buffer=BUFFER_SIZE)
    
    print(f"Starting noise cancellation for {target_frequency} Hz ± {bandwidth/2} Hz. Press Ctrl+C to stop.")
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Real-Time Noise Cancellation")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    line1, = ax.plot([], [], label="Original Signal")
    line2, = ax.plot([], [], label="Filtered Signal", color="orange")
    ax.legend()

    try:
        with open(LOG_FILE, 'w', newline='') as logfile:
            log_writer = csv.writer(logfile)
            log_writer.writerow(["Timestamp", "Target Frequency (Hz)", "Processing Time (ms)"])
            
            while True:
                data = np.frombuffer(stream.read(BUFFER_SIZE, exception_on_overflow=False), dtype=np.int16)
                filtered_data = band_stop_filter(data, target_frequency - bandwidth/2, target_frequency + bandwidth/2, sampling_rate)

                # Visualization
                line1.set_ydata(data)
                line1.set_xdata(np.linspace(0, len(data) / sampling_rate, len(data)))
                line2.set_ydata(filtered_data)
                line2.set_xdata(np.linspace(0, len(filtered_data) / sampling_rate, len(filtered_data)))
                ax.relim()
                ax.autoscale_view()
                plt.pause(0.01)

                # Logging
                processing_time = round(time.time() * 1000)
                log_writer.writerow([time.time(), target_frequency, processing_time])
    except KeyboardInterrupt:
        print("\nStopping noise cancellation.")
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        plt.ioff()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Noise Cancellation Script")
    parser.add_argument("--target_frequency", type=float, required=True, help="Target frequency for cancellation (Hz)")
    parser.add_argument("--bandwidth", type=float, default=50, help="Bandwidth for the band-stop filter (Hz)")
    parser.add_argument("--sampling_rate", type=int, default=DEFAULT_SAMPLING_RATE, help="Sampling rate (Hz)")
    parser.add_argument("--buffer_size", type=int, default=BUFFER_SIZE, help="Buffer size for real-time audio processing")
    args = parser.parse_args()

    process_audio_stream(args.target_frequency, args.bandwidth, args.sampling_rate)