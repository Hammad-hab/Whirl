"""The player's rocket: state, controls and per-frame flight integration."""
import math

from .config import (BOOST_DRAIN, BOOST_MAX, DRAG, DT, GRAVITY, MAX_V, THRUST, THRUST_HOLD,
                     TURN, TURN_HOLD)


class Rocket:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.th = self.om = 0.0            # angle (rad, 0 = nose up) and angular velocity
        self.boost = BOOST_MAX
        self.thr = self.lt = self.rt = 0   # frames of "key held" remaining
        self.latch = False
        self.thrusting = False
        self.checkpoint = (x, y)

    # ---- controls (called by input actions) ----
    def press_thrust(self):
        self.thr = THRUST_HOLD

    def press_left(self):
        self.lt = TURN_HOLD

    def press_right(self):
        self.rt = TURN_HOLD

    def toggle_latch(self):
        self.latch = not self.latch

    # ---- simulation ----
    def step(self, bio, particles):
        """Thrust, rotation, gravity, drag and position update (collisions happen later)."""
        self.thrusting = (self.thr > 0 or self.latch) and self.boost > 10
        sn, cs = math.sin(self.th), math.cos(self.th)
        ax = ay = 0.0
        if self.thrusting:
            ax, ay = sn * THRUST, -cs * THRUST
            self.boost -= BOOST_DRAIN * DT
            particles.exhaust(self)
        tgt = 0.0
        if self.lt > 0 and self.rt <= 0:
            tgt = -TURN
        elif self.rt > 0 and self.lt <= 0:
            tgt = TURN
        self.om += (tgt - self.om) * min(1.0, 10 * DT)
        self.th += self.om * DT
        self.th = (self.th + math.pi) % (2 * math.pi) - math.pi
        self.thr = max(0, self.thr - 1)
        self.lt = max(0, self.lt - 1)
        self.rt = max(0, self.rt - 1)
        self.vx += ax * DT
        self.vy += (GRAVITY * bio.grav + ay) * DT
        self.vx *= 1 - DRAG * DT
        self.vy *= 1 - DRAG * DT
        sp = math.hypot(self.vx, self.vy)
        if sp > MAX_V:
            self.vx, self.vy = self.vx * MAX_V / sp, self.vy * MAX_V / sp
        self.x += self.vx * DT
        self.y += self.vy * DT

    def respawn(self):
        self.x, self.y = self.checkpoint
        self.vx = self.vy = self.th = self.om = 0.0
        self.boost = BOOST_MAX
