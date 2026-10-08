"""Ambient biome particles (fireflies, snow...). Add one with @effect("name"), then set
`fx="name"` on a Biome. They live in the level, wrap around their zone, and are cosmetic."""
import math
import random

from .config import DT

EFFECTS = {}


def effect(name):
    def deco(cls):
        EFFECTS[name] = cls
        return cls
    return deco


class Ambient:
    @classmethod
    def y_range(cls, H):
        """Spawn band in rows."""
        return 2, H - 4

    def __init__(self, x, y, phase, lo, hi, biome):
        self.x, self.y, self.phase = x, y, phase
        self.lo, self.hi, self.biome = lo, hi, biome
        self.vx = self.vy = 0.0
        self.anchor = y

    def update(self, frame, H):
        self.step(frame, H)
        if self.x > self.hi:
            self.x = self.lo
        elif self.x < self.lo:
            self.x = self.hi

    def step(self, frame, H):
        pass

    def color(self):
        cols = self.biome.fxc
        return cols[int(self.phase * 7) % len(cols)]

    def draw(self, cv, cx, cy, frame):
        pass


class Wander(Ambient):
    """Lazy random walk inside a band measured up from the bottom of the screen."""
    OFF = (-17, -4)

    @classmethod
    def y_range(cls, H):
        return H + cls.OFF[0], H + cls.OFF[1]

    def step(self, frame, H):
        lo, hi = self.OFF
        self.vx = max(-1.5, min(1.5, self.vx + random.uniform(-1, 1) * 3 * DT))
        self.vy = max(-1.0, min(1.0, self.vy + random.uniform(-1, 1) * 3 * DT))
        self.x += self.vx * DT
        self.y = max(H + lo, min(H + hi, self.y + self.vy * DT))

    def draw(self, cv, cx, cy, frame):
        if math.sin(frame * 0.12 + self.phase) > 0.1:
            col = self.color()
            cv.dot(cx, cy, col)
            cv.dot(cx + 1, cy, col)


@effect("firefly")
class Firefly(Wander):
    OFF = (-17, -4)


@effect("spore")
class Spore(Wander):
    OFF = (-20, -5)


@effect("snow")
class Snow(Ambient):
    def step(self, frame, H):
        self.x += math.sin(frame * 0.06 + self.phase) * 1.2 * DT
        self.y += 3.0 * DT
        if self.y > H - 3:
            self.y = 1.0

    def draw(self, cv, cx, cy, frame):
        col = self.color()
        for ddx in (0, 1):
            for ddy in (0, 1):
                cv.dot(cx + ddx, cy + ddy, col)


@effect("ember")
class Ember(Ambient):
    def step(self, frame, H):
        self.x += math.sin(frame * 0.1 + self.phase) * 2.0 * DT
        self.y -= 3.5 * DT
        if self.y < 2:
            self.y = H - 4

    def draw(self, cv, cx, cy, frame):
        if math.sin(frame * 0.3 + self.phase) > -0.5:
            col = self.color()
            cv.dot(cx, cy, col)
            cv.dot(cx, cy + 1, col)


@effect("dust")
class Dust(Ambient):
    @classmethod
    def y_range(cls, H):
        return H - 14, H - 5

    def step(self, frame, H):
        self.x += 7.0 * DT
        self.y = self.anchor + 0.8 * math.sin(frame * 0.1 + self.phase)

    def draw(self, cv, cx, cy, frame):
        col = self.color()
        cv.dot(cx, cy, col)
        cv.dot(cx + 1, cy, col)


def spawn_ambient(zones, edges, H):
    """Create ambient particles for every zone of a level."""
    out = []
    for i, bio in enumerate(zones):
        cls = EFFECTS.get(bio.fx)
        if cls is None:
            continue
        lo, hi = edges[i], edges[i + 1]
        y0, y1 = cls.y_range(H)
        for _ in range(int((hi - lo) * bio.fxn)):
            out.append(cls(random.uniform(lo, hi), random.uniform(y0, y1),
                           random.uniform(0, 6.28), lo, hi, bio))
    return out
