import json
import time
from collections import deque
from pathlib import Path

import joblib
import keyboard
import numpy as np
import pyttsx3

MODEL_PATH = "sign_language_rf_model.pkl"
CALIBRATION_PATH = Path("calibration.json")

WINDOW_SIZE = 7
STABLE_FRAMES = 6
CONFIDENCE_THRESHOLD = 0.65
LOOP_DELAY = 0.05

FEATURE_COUNT = 5

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

model = joblib.load(MODEL_PATH)

window = deque(maxlen=WINDOW_SIZE)
prev_letter = None
stable_count = 0
word = ""

last_space = False
last_r = False


def get_sensor_values():
    """Placeholder for real sensor data. Returns 5 floats."""
    return np.random.rand(FEATURE_COUNT)


def load_calibration():
    if not CALIBRATION_PATH.exists():
        print("Calibration file not found. Running without normalization.")
        return None

    try:
        data = json.loads(CALIBRATION_PATH.read_text())
        open_vals = np.asarray(data["open"], dtype=float)
        closed_vals = np.asarray(data["closed"], dtype=float)
        if open_vals.shape[0] != FEATURE_COUNT or closed_vals.shape[0] != FEATURE_COUNT:
            print("Calibration has wrong feature count. Ignoring it.")
            return None
        print("Calibration loaded.")
        return {"open": open_vals, "closed": closed_vals}
    except Exception:
        print("Failed to load calibration. Running without normalization.")
        return None


def apply_calibration(values, calibration):
    if calibration is None:
        return values

    open_vals = calibration["open"]
    closed_vals = calibration["closed"]
    span = closed_vals - open_vals
    span = np.where(np.abs(span) < 1e-6, 1e-6, span)
    normalized = (values - open_vals) / span
    return np.clip(normalized, 0.0, 1.0)


def reset_state():
    global prev_letter, stable_count, word
    prev_letter = None
    stable_count = 0
    word = ""


def speak_word(text):
    if not text:
        return
    engine.say(text)
    engine.runAndWait()


def status_line(letter, confidence, current_word):
    letter_display = letter if letter else "-"
    return f"LETTER: {letter_display} | CONF: {confidence:.2f} | WORD: {current_word}"


calibration = load_calibration()

print("SIGN LANGUAGE TRANSLATOR GLOVE")
print("Controls: SPACE = speak word, R = reset, Ctrl+C = exit")
print("Waiting for sensor data...\n")

while True:
    raw_values = np.asarray(get_sensor_values(), dtype=float)
    if raw_values.shape[0] != FEATURE_COUNT:
        print("\nSensor input error: expected 5 values.")
        time.sleep(1)
        continue

    values = apply_calibration(raw_values, calibration)
    window.append(values)

    if len(window) < WINDOW_SIZE:
        time.sleep(LOOP_DELAY)
        continue

    avg = np.mean(window, axis=0)

    # Keyboard controls with edge detection
    space_pressed = keyboard.is_pressed("space")
    if space_pressed and not last_space:
        print("\nSPEAK:", word if word else "(empty)")
        speak_word(word)
        reset_state()
    last_space = space_pressed

    r_pressed = keyboard.is_pressed("r")
    if r_pressed and not last_r:
        print("\nRESET")
        reset_state()
    last_r = r_pressed

    probs = model.predict_proba(avg.reshape(1, -1))[0]
    confidence = float(np.max(probs))
    letter = model.classes_[int(np.argmax(probs))]

    if confidence < CONFIDENCE_THRESHOLD:
        prev_letter = None
        stable_count = 0
        letter_out = None
    else:
        if letter == prev_letter:
            stable_count += 1
        else:
            stable_count = 1
            prev_letter = letter

        if stable_count >= STABLE_FRAMES:
            word += letter
            stable_count = 0
            prev_letter = None

        letter_out = letter

    line = status_line(letter_out, confidence, word)
    print("\r" + line.ljust(80), end="", flush=True)
    time.sleep(LOOP_DELAY)
