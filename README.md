# Sign Language Recognition using Flex Sensors (5 Sensor System)

## Overview
This project detects hand gestures using 5 flex sensors and a machine learning model.

## System Flow
Flex Sensors → Arduino → Serial → Python → ML Model → Output

## Components
- Arduino Nano
- 5 Flex Sensors (Thumb, Index, Middle, Ring, Little)
- Python ML Model (Random Forest)

## Model
Random Forest Classifier

## How to Run
1. Upload Arduino code
2. Install dependencies:
   pip install -r requirements.txt
3. Train model:
   python train_model.py
4. Run prediction:
   python live_predict.py