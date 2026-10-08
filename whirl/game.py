"""Game state + the per-frame update loop. Rules live in systems.py, reactions in handlers."""
import random

from .camera import Camera
from .colors import YEL
from .config import CRASH_TIME, DT, R, SHAKE_FRAMES
from .events import EventBus
from .level import Level
from .particles import FloatingTexts, ParticleSystem
from . import physics
from .rocket import Rocket
from .systems import AmbientFx, GoalWatcher, GroundContact, StarCollector, WinConfetti


class Game:
    def __init__(self, W, H, biome):
        self.W, self.H = W, H
        self.level = Level(W, H, biome)
        p = self.level.plats[0]
        self.rocket = Rocket(p.x + p.w / 2, p.y - R - 0.01, biome)
        self.camera = Camera(W)
        self.camera.snap(self.rocket, self.level.Wu)
        self.particles = ParticleSystem()
        self.texts = FloatingTexts()
        self.events = EventBus()
        # rules
        self.flying_systems = [GroundContact(), StarCollector(), GoalWatcher()]
        self.systems = [WinConfetti(), AmbientFx()]
        # state
        self.status = "flying"          # flying | crashed
        self.timer = 0.0
        self.got = 0
        self.won = False
        self.started = False
        self.grounded = False
        self.shake = 0
        self.frame = 0
        self.cur = 0                    # current biome zone
        self.btime = 0.0                # biome banner timer
        install_default_handlers(self)

    # ---- helpers ----
    @property
    def biome(self):
        return self.level.zones[self.cur]

    @property
    def total_stars(self):
        return len(self.level.stars)

    def emit(self, name, **info):
        self.events.emit(name, self, **info)

    def crash(self):
        self.status = "crashed"
        self.timer = CRASH_TIME
        self.rocket.thrusting = False
        self.emit("crash")

    # ---- per-frame ----
    def _track_zone(self):
        slot = self.level.slot_at(int(2 * self.rocket.x), False)
        if slot != self.cur:
            self.cur = slot
            self.btime = 2.5
            self.emit("biome_enter", biome=self.biome)
        self.btime = max(0.0, self.btime - DT)

    def update(self):
        self.frame += 1
        self._track_zone()
        r = self.rocket
        if self.status == "flying":
            r.step(self.particles)
            self.grounded, crashed = physics.resolve(r, self.level.solids, self.particles)
            if crashed:
                self.crash()
            else:
                physics.clamp_to_world(r, self.level.Wu)
                for s in self.flying_systems:
                    s.update(self)
        elif self.status == "crashed":
            self.timer -= DT
            if self.timer <= 0:
                r.respawn()
                self.status = "flying"
        if self.shake > 0:
            self.shake -= 1
        for s in self.systems:
            s.update(self)
        self.particles.update(self.level.Wu, self.H)
        self.texts.update()
        self.camera.follow(r, self.level.Wu)


# ---- default reactions to events (swap/extend these to change juice without touching rules) ----
def install_default_handlers(game):
    ev = game.events

    @ev.on("star")
    def _star(g, star):
        g.particles.burst(star.x, star.y, 14, 9)
        g.texts.add(star.x, star.y - 1, "+1", YEL)

    @ev.on("crash")
    def _crash(g):
        g.particles.burst(g.rocket.x, g.rocket.y, 90)
        g.shake = SHAKE_FRAMES

    @ev.on("win")
    def _win(g):
        gx, gy = g.level.goal
        for _ in range(5):
            g.particles.burst(gx + random.uniform(-6, 6), gy - random.uniform(5, 12), 40, 14)
