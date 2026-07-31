print("Step 1")

import cv2
print("Step 2 - OpenCV imported")

import mediapipe as mp
print("Step 3 - MediaPipe imported")

print("MediaPipe:", mp.__version__)
print("Tasks available:", hasattr(mp, "tasks"))
print("Solutions available:", hasattr(mp, "solutions"))

cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("Step 4 - Camera opened")
else:
    print("Step 4 - Camera failed")

cap.release()

print("Step 5 - Finished")