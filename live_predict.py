import joblib
import numpy as np

# Load model
model = joblib.load("model.pkl")

print("Choose mode:")
print("1 → Manual Input (No Arduino)")
print("2 → Arduino Mode")

mode = input("Enter mode (1/2): ")

# ---------------------------
# MANUAL MODE (NO HARDWARE)
# ---------------------------
if mode == "1":
    print("Enter 5 sensor values: S1,S2,S3,S4,S5")

    while True:
        try:
            user_input = input("Values: ")
            values = list(map(int, user_input.split(",")))

            if len(values) != 5:
                print("Enter exactly 5 values")
                continue

            X = np.array([values])
            prediction = model.predict(X)[0]

            print("Gesture:", prediction)

        except:
            print("Invalid input")

# ---------------------------
# ARDUINO MODE
# ---------------------------
elif mode == "2":
    import serial
    from collections import deque

    ser = serial.Serial("COM3", 9600)  # change COM if needed
    window = deque(maxlen=5)

    print("Listening from Arduino...")

    while True:
        try:
            line = ser.readline().decode().strip()
            values = list(map(int, line.split(",")))

            if len(values) != 5:
                continue

            X = np.array([values])

            probs = model.predict_proba(X)[0]
            pred = model.classes_[np.argmax(probs)]
            confidence = max(probs)

            window.append(pred)

            if len(window) == 5:
                final = max(set(window), key=window.count)

                if confidence > 0.6:
                    print("Gesture:", final)

        except:
            continue