# Levi Labs — Hand Gesture Particle System

A real-time computer vision project that uses hand tracking and pinch gestures to create an interactive fairy-dust particle effect with a colorful radial burst.

## Overview

Levi Labs is an interactive hand-gesture visualization project built with Python, OpenCV, and MediaPipe.

The application tracks hand landmarks through a webcam and detects a pinch gesture between the thumb and index finger. Normal hand movement produces a continuous fairy-dust trail, while a pinch triggers a short-lived colorful particle burst.

The project combines computer vision, gesture detection, particle physics, animation, and real-time rendering into a single interactive application.

## Features

- Real-time hand tracking using MediaPipe
- Pinch gesture detection using thumb–index finger distance
- Continuous fairy-dust particle emission from the index fingertip
- Colorful radial particle burst triggered by a pinch
- Particle movement with velocity and lightweight physics
- Particle lifetime, shrinking, fading, and glow effects
- Subtle star-like particle twinkling
- Separate behavior for normal fairy-dust and explosion particles
- Real-time OpenCV rendering through a webcam

## Technology Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- Mathematical particle simulation

## How It Works

1. The webcam captures a live video frame.
2. MediaPipe detects the hand and provides 21 hand landmarks.
3. The thumb tip and index fingertip coordinates are extracted.
4. The Euclidean distance between the two fingertips is calculated.
5. If the distance falls below the pinch threshold, a pinch gesture is detected.
6. Normal hand movement continuously generates fairy-dust particles.
7. A pinch triggers a radial burst of colored explosion particles.
8. Each particle is updated every frame according to its velocity and lifetime.
9. Particle size and brightness decrease over time while a subtle twinkle effect is applied.
10. OpenCV combines the particle layers and glow effects with the webcam frame.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Lab001_HandGestureParticles
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py

## Hand Landmarker Model

This project uses the MediaPipe Hand Landmarker model for real-time hand landmark detection.
The required model file is:

`hand_landmarker.task`

Place the model file in the project root directory alongside `main.py` before running the application.

## Project Structure

```text
Lab001_HandGestureParticles/
│
├── main.py
├── particle.py
├── hand_landmarker.task
├── requirements.txt
├── README.md
└── .gitignore

## Future Improvements

- Support for additional hand gestures
- More interactive particle effects
- Customizable particle themes and colors
- Additional gesture-triggered visual effects
- Performance optimization for higher-resolution video

## Author

Rebekah Russel

Data Science | Machine Learning | Computer Vision
