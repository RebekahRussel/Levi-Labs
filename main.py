# =========================
# Imports
# =========================
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import RunningMode
import time
from particle import Particle
import numpy as np
import random
import math

# =========================
# Hand Landmark Connections
# =========================
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),

    (0, 5), (5, 6), (6, 7), (7, 8),

    (0, 9), (9, 10), (10, 11), (11, 12),

    (0, 13), (13, 14), (14, 15), (15, 16),

    (0, 17), (17, 18), (18, 19), (19, 20),

    (5, 9), (9, 13), (13, 17)
]

# =========================
# Particle Settings
# =========================

EMISSION_RATE = 5
EXPLOSION_COUNT = 50

# Pinch Detection
PINCH_THRESHOLD = 25

# Explosion Settings
EXPLOSION_SPEED_MIN = 3.0
EXPLOSION_SPEED_MAX = 4.5
EXPLOSION_RADIUS_MIN = 5
EXPLOSION_RADIUS_MAX = 7
EXPLOSION_RAY_COUNT = 8

EXPLOSION_COLORS = [
    (255, 80, 80),
    (100, 180, 255),
    (255, 180, 80),
    (220, 100, 255),
    (120, 255, 180)
]

# Runtime State
pinching = False

# =========================
# Hand Tracking Setup
# =========================
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

# =========================
# Camera & Particle Setup
# =========================
cap=cv2.VideoCapture(0)
particles=[]

# =========================
# Main Processing Loop
# =========================
while cap.isOpened():
    success, frame=cap.read()
    glow_frame=np.zeros_like(frame)
    particle_glow_frame=np.zeros_like(frame)

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
    
# -------------------------
# Hand Detection & Gestures
# -------------------------
    height,width, _=frame.shape
    if result.hand_landmarks:
        for hand in result.hand_landmarks:

            thumb_tip=hand[4]
            index_tip=hand[8]

            thumb_x=int(thumb_tip.x * width)
            thumb_y=int(thumb_tip.y * height)

            x=int(index_tip.x * width)
            y=int(index_tip.y * height)

            dx=x-thumb_x
            dy=y-thumb_y

            distance=math.hypot(dx, dy)

            if distance<PINCH_THRESHOLD:
                if not pinching:
                    pinching=True

                    explosion_x=(thumb_x + x)//2
                    explosion_y=(thumb_y + y)//2

                    ray_count = EXPLOSION_RAY_COUNT
                    particles_per_ray=EXPLOSION_COUNT // ray_count

                    for i in range(EXPLOSION_COUNT):
                        ray_index= i // particles_per_ray
                        base_angle=(2*math.pi / ray_count) * ray_index
                        angle=base_angle + random.uniform(-0.08, 0.08)

                        speed = random.uniform(
                            EXPLOSION_SPEED_MIN,
                            EXPLOSION_SPEED_MAX
                        )

                        vx=math.cos(angle)*speed
                        vy=math.sin(angle)*speed

                        life=random.randint(45,70)

                        radius = random.randint(
                            EXPLOSION_RADIUS_MIN,
                            EXPLOSION_RADIUS_MAX
                        )

                        explosion_color=random.choice(EXPLOSION_COLORS)

                        spawn_distance= 3

                        particle_x=explosion_x + math.cos(angle) * spawn_distance
                        particle_y=explosion_y + math.sin(angle) * spawn_distance
                        particles.append(
                            Particle(particle_x,particle_y,vx,vy,life,explosion_color,radius,True)
                        )
            else:
                pinching=False


            if not pinching:
                for i in range(EMISSION_RATE):
                    spawn_x= x+random.randint(-5,5)
                    spawn_y= y+random.randint(-5,5)
                    particles.append(Particle(spawn_x,spawn_y))
            
            for start,end in HAND_CONNECTIONS:
                start_landmark=hand[start]
                end_landmark=hand[end]

                x1=int(start_landmark.x*width)
                y1=int(start_landmark.y*height)

                x2=int(end_landmark.x*width)
                y2=int(end_landmark.y*height)

                cv2.line(
                    glow_frame,
                    (x1,y1),
                    (x2,y2),
                    (80,255,255),
                    8
                )
                cv2.line(
                    glow_frame,
                    (x1,y1),
                    (x2,y2),
                    (180,255,255),
                    4
                )
                cv2.line(
                    glow_frame,
                    (x1,y1),
                    (x2,y2),
                    (255,255,255),
                    2
                )

            for landmark in hand:
                x=int(landmark.x*width)
                y=int(landmark.y*height)

                cv2.circle(
                    glow_frame,
                    (x,y),
                    6,
                    (255,255,0),
                    -1
                )
# -------------------------
# Frame & Particle Rendering
# -------------------------
    blurred_glow=cv2.GaussianBlur(
        glow_frame,
        (31,31),
        0
        )
 
    final_frame=cv2.addWeighted(
        frame,
        1.0,
        blurred_glow,
        0.8,
        0
        )
  
    alive_particles=[]
    for particle in particles:
        particle.update()

        if particle.is_alive():
            particle.draw(final_frame)
            particle.draw(particle_glow_frame,glow=True)
            alive_particles.append(particle)

    particles =alive_particles
    particle_blurred_glow=cv2.GaussianBlur(
            particle_glow_frame,
            (31,31),
            0
        )
    result_frame=cv2.addWeighted(
            final_frame,
            1.0,
            particle_blurred_glow,
            0.8,
            0
        )
    cv2.imshow("Levi Labs Hand Tracker", result_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =========================
# Cleanup
# =========================
cap.release()
cv2.destroyAllWindows()