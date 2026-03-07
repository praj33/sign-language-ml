# Sign Language Translator Glove

Hackathon-ready software stack that maps 5 flex sensor readings to letters using a machine learning model, builds words from stable predictions, and speaks completed words.

## Features
- RandomForestClassifier trained on flex sensor readings
- Sliding window smoothing with confidence threshold
- Stable frame counter to reduce jitter
- Word building from predicted letters
- Text-to-speech for whole words only
- Keyboard controls for speak and reset
- Modular sensor input stub for Arduino or ESP32 integration

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Train the model: `python train_model.py`
3. Start live prediction: `python live_predict.py`

## Demo Controls
- `SPACE` speaks the current word
- `R` resets the current word
- `Ctrl+C` exits

## Future Work
- Replace `get_sensor_values()` with real serial data from Arduino/ESP32
- Add calibration and normalization per user
- Expand dataset to cover more letters and gestures
- Add a language model for autocorrect and phrase suggestions
- Build a lightweight UI for accessibility
