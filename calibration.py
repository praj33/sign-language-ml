import json
import time
from pathlib import Path

import numpy as np

CALIBRATION_PATH = Path("calibration.json")
FEATURE_COUNT = 5
SAMPLES_PER_POSE = 60
SAMPLE_DELAY = 0.03


def get_sensor_values():
    """Placeholder for real sensor data. Returns 5 floats."""
    return np.random.rand(FEATURE_COUNT)


def countdown(seconds=3):
    for i in range(seconds, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)


def collect_baseline(label):
    print(f"\nHold {label} pose and press Enter to start sampling.")
    input()
    countdown(3)

    samples = []
    for _ in range(SAMPLES_PER_POSE):
        values = np.asarray(get_sensor_values(), dtype=float)
        if values.shape[0] != FEATURE_COUNT:
            raise ValueError("Sensor values must have 5 elements.")
        samples.append(values)
        time.sleep(SAMPLE_DELAY)

    mean_values = np.mean(samples, axis=0)
    print(f"{label} baseline captured: {mean_values}")
    return mean_values


def save_calibration(open_vals, closed_vals):
    data = {
        "feature_count": FEATURE_COUNT,
        "open": open_vals.tolist(),
        "closed": closed_vals.tolist(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    CALIBRATION_PATH.write_text(json.dumps(data, indent=2))
    print(f"\nCalibration saved to {CALIBRATION_PATH}")


def main():
    print("SIGN GLOVE CALIBRATION")
    print("This will record two baselines: open hand and closed hand.")
    print("Make sure your glove is connected and stable.\n")

    open_vals = collect_baseline("OPEN HAND")
    closed_vals = collect_baseline("CLOSED HAND")

    span = closed_vals - open_vals
    if np.any(np.abs(span) < 1e-6):
        print("\nWarning: Some sensors have near-zero range.")
        print("Check your glove placement and try again if needed.")

    save_calibration(open_vals, closed_vals)


if __name__ == "__main__":
    main()
