import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import RunningMode
import time

HAND_CONNECTIONS = [
    # Thumb
    (0, 1), (1, 2), (2, 3), (3, 4),

    # Index finger
    (0, 5), (5, 6), (6, 7), (7, 8),

    # Middle finger
    (0, 9), (9, 10), (10, 11), (11, 12),

    # Ring finger
    (0, 13), (13, 14), (14, 15), (15, 16),

    # Pinky
    (0, 17), (17, 18), (18, 19), (19, 20),

    # Palm
    (5, 9), (9, 13), (13, 17)
]

print("Levi Labs - Hand Tracker")
base_options=BaseOptions(
    model_asset_path="hand_landmarker.task"
)
options=vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.1,
    min_hand_presence_confidence=0.1,
    min_tracking_confidence=0.1
)
hand_landmarker=vision.HandLandmarker.create_from_options(options)

cap=cv2.VideoCapture(0)
while cap.isOpened():
    success, frame=cap.read()
    print(frame.shape)

    if not success:
        break

    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    mp_image=mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )
    timestamp_ms=int(time.perf_counter()*1000)
    result=hand_landmarker.detect_for_video(
        mp_image,
        timestamp_ms
    )
    print("Hands detected:", len(result.hand_landmarks))

    height,width, _=frame.shape
    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            for start,end in HAND_CONNECTIONS:
                start_landmark=hand[start]
                end_landmark=hand[end]

                x1=int(start_landmark.x*width)
                y1=int(start_landmark.y*height)

                x2=int(end_landmark.x*width)
                y2=int(end_landmark.y*height)

                cv2.line(
                    frame,
                    (x1,y1),
                    (x2,y2),
                    (225,255, 0),
                    2
                )

            for landmark in hand:
                x=int(landmark.x*width)
                y=int(landmark.y*height)

                cv2.circle(
                    frame,
                    (x,y),
                    6,
                    (255,255,0),
                    -1
                )
    

    cv2.imshow("Levi Labs Hand Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()