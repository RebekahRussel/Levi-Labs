import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
hands=mp_hands.Hands()
mp_draw=mp.solutions.drawing_utils

cap=cv2.VideoCapture(0)

while True:
    success, frame=cap.read()
    if not success:
        break
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results=hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        print("Hand Detected")


    cv2.imshow("Levi Labs-Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
