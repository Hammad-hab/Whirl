"""Short-lived particles (fire, smoke, confetti) and floating text.

Add a particle kind by adding an entry to KINDS (gravity scale + colour-by-age function),
then spawn it with ParticleSystem.add("kind", ...).
"""
import math
import random
from dataclasses import dataclass
from typing import Callable

from .colors import GRY, ORG, RED, WHT, YEL, CONFETTI, cp
from .config import DT, GRAVITY, R
from .gfx.term import put


@dataclass
class Kind:
    gravity: float                         # multiplier on GRAVITY
    color: Callable                        # (particle, remaining_ratio) -> colour id
    hide_below: float = 0.0                # skip drawing when remaining ratio is under this


KINDS = {
    "fire": Kind(0.7, lambda p, r: WHT if r > 0.85 else YEL if r > 0.6 else ORG if r > 0.3 else RED),
    "smoke": Kind(0.0, lambda p, r: GRY, hide_below=0.12),
    "confetti": Kind(0.2, lambda p, r: p.color),
}


class Particle:
    __slots__ = ("kind", "x", "y", "vx", "vy", "life", "maxlife", "color")

    def __init__(self, kind, x, y, vx, vy, life, color=None):
        self.kind, self.x, self.y, self.vx, self.vy = kind, x, y, vx, vy
        self.life = self.maxlife = life
        self.color = color


class ParticleSystem:
    def __init__(self):
        self.items = []

    def add(self, kind, x, y, vx, vy, life, color=None):
        self.items.append(Particle(kind, x, y, vx, vy, life, color))

    # ---- emitters ----
    def burst(self, x, y, n, speed=18.0):
        for _ in range(n):
            a = random.uniform(0, 2 * math.pi)
            sp = random.uniform(2, speed)
            self.add("fire", x, y, math.cos(a) * sp, math.sin(a) * sp * 0.8 - 3,
                     random.uniform(0.5, 1.4))

    def exhaust(self, rocket):
        sn, cs = math.sin(rocket.th), math.cos(rocket.th)
        for _ in range(2):
            sp = random.uniform(4, 9)
            self.add("smoke", rocket.x - 1.7 * sn, rocket.y + 1.7 * cs,
                     -sn * sp + rocket.vx * 0.4 + random.uniform(-1.5, 1.5),
                     cs * sp + rocket.vy * 0.4 + random.uniform(-1.5, 1.5),
                     random.uniform(0.4, 0.9))

    def landing_puff(self, rocket):
        for _ in range(8):
            self.add("smoke", rocket.x + random.uniform(-1.5, 1.5), rocket.y + R - 0.3,
                     random.uniform(-5, 5), random.uniform(-2, 0), 0.5)

    def confetti(self, cx):
        for _ in range(3):
            self.add("confetti", cx + random.uniform(-12, 12), 1.0,
                     random.uniform(-2, 2), random.uniform(2, 5), 2.8, random.choice(CONFETTI))

    # ---- simulation / drawing ----
    def update(self, level_w, H):
        alive = []
        for p in self.items:
            p.vy += GRAVITY * KINDS[p.kind].gravity * DT
            p.x += p.vx * DT
            p.y += p.vy * DT
            p.life -= DT
            if p.life <= 0 or not (0 <= p.x < level_w) or p.y >= H - 2:
                continue
            alive.append(p)
        self.items = alive

    def draw(self, cv, cam):
        for p in self.items:
            k = KINDS[p.kind]
            r = p.life / p.maxlife
            if r < k.hide_below:
                continue
            col = k.color(p, r)
            dx, dy = int(p.x * 4) - cam * 2, int(p.y * 4)
            cv.dot(dx, dy, col)
            if r > 0.55:
                cv.dot(dx + 1, dy, col)
                cv.dot(dx, dy + 1, col)
                cv.dot(dx + 1, dy + 1, col)


class FloatingTexts:
    def __init__(self):
        self.items = []     # [x, y, life, text, colour]

    def add(self, x, y, text, col):
        self.items.append([x, y, 1.0, text, col])

    def update(self):
        for t in self.items:
            t[1] -= 3 * DT
            t[2] -= DT
        self.items = [t for t in self.items if t[2] > 0]

    def draw(self, s, cam):
        for tx, ty, _, txt, col in self.items:
            put(s, int(ty), int(2 * tx) - cam, txt, cp(col, True))
