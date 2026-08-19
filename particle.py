# =========================
# Imports
# =========================
import cv2
import random
import math

# =========================
# Particle Class
# =========================
class Particle:
    def __init__(self,x,y,vx=None, vy=None, life=None, color=None, radius=None, explosion=False):
        self.x=x
        self.y=y

        velocities = [-3, -2, -1, 1, 2, 3]

        if vx is not None:
            self.vx=vx
        else:
            self.vx=random.choice(velocities)

        if vy is not None:
            self.vy=vy
        else:
            self.vy=random.choice(velocities)

        if life is not None:
            self.life=life
        else:   
            self.life=random.randint(80,120)

        default_colors = [
        (255, 255, 255),   
        (255, 220, 100),   
        (255, 180, 255),   
        (255, 255, 120),   
        (255, 220, 220)    
        ]
        
        if color is not None:
            self.color=color
        else:
            self.color=random.choice(default_colors)

        if radius is not None:
            self.radius=radius
        else:
            self.radius=None
        

        self.explosion=explosion

        self.twinkle_speed=random.uniform(0.15, 0.3)
        self.twinkle_phase=random.uniform(0, 2*math.pi)
        self.twinkle_time=0

    def update(self):

        if not self.explosion:
            self.vx+=random.uniform(-0.05,0.05)
            self.vy+=random.uniform(-0.05,0.05)

            self.vy-=0.02

        self.x += self.vx
        self.y += self.vy

        self.life-=1

        self.twinkle_time += self.twinkle_speed
        

    def draw(self,frame,glow=False):
        # Normalize lifetime for fading and shrinking
        life=self.life/100

        # Apply lifetime fade to particle color
        r=int(self.color[0]*life)
        g=int(self.color[1]*life)
        b=int(self.color[2]*life)

        # Calculate the particle's base size
        if self.radius is not None:
            base_radius=self.radius
        else:   
            base_radius=3

        # Add a subtle star-like twinkle
        twinkle=1+0.15 * math.sin(self.twinkle_time + self.twinkle_phase)
        brightness=int(255 * life * twinkle)

        # Particle shrinks as its lifetime decreases
        radius = max(1, int(base_radius * life * twinkle))
        glow_radius=radius+1

        # Stop rendering particles once they become too faint
        # to avoid dark particles appearing before disappearance.
        if brightness>80:
            # Explosion particles retain their assigned colors.
            # Normal fairy dust keeps the original white appearance.
            if glow:
                color=(b,g,r)
                circle_radius=glow_radius
            else:
                if self.explosion:
                    color=(b,g,r)
                else:
                    color=(255,255,255)

                circle_radius=radius
           
            cv2.circle(
                frame,
                (int(self.x),int(self.y)),
                circle_radius,
                color,
                -1
                )

    def is_alive(self):
        return self.life>0
            