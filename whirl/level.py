"""Procedural level: platforms, collectibles, goal, decorations, biome zones, scenery."""
import random
from dataclasses import dataclass
from typing import NamedTuple

from . import config as cfg
from .effects import spawn_ambient


class Platform(NamedTuple):
    x: float
    y: float
    w: float


@dataclass
class Star:
    x: float
    y: float
    got: bool = False


class Level:
    def __init__(self, W, H, biome):
        """`biome` is a Biome (one zone) or a list of Biomes (zones laid out left to right)."""
        self.W, self.H = W, H
        self._platforms()
        self._zones(biome)
        self._pickups()
        self._decorations()
        self._scenery()
        self.ambient = spawn_ambient(self.zones, self.edges, H)

    # ---- generation ----
    def _platforms(self):
        H = self.H
        x, y = 4, H - 9
        self.plats = [Platform(x, y, cfg.START_PLATFORM_W)]
        for _ in range(cfg.NUM_PLATFORMS):
            x += self.plats[-1].w + random.randint(*cfg.PLATFORM_GAP)
            y = max(6, min(H - 8, y + random.randint(-cfg.PLATFORM_DY, cfg.PLATFORM_DY)))
            self.plats.append(Platform(x, y, random.randint(*cfg.PLATFORM_W)))
        last = self.plats[-1]
        self.Wu = last.x + last.w + cfg.LEVEL_TAIL
        self.solids = [(0, H - 2, self.Wu, 3)] + [(p.x, p.y, p.w, 2) for p in self.plats]
        self.goal = (last.x + last.w / 2, last.y)

    def _zones(self, biome):
        self.zones = list(biome) if isinstance(biome, (list, tuple)) else [biome]
        n = len(self.zones)
        self.edges = [self.Wu * i / n for i in range(n + 1)]          # units
        self.bounds = [2 * e for e in self.edges[1:-1]]               # columns
        self.centers = [self.edges[i] + self.edges[i + 1] for i in range(n)]   # columns

    def _pickups(self):
        self.stars = []
        for i in range(1, len(self.plats)):
            p, q = self.plats[i], self.plats[i - 1]
            self.stars.append(Star(p.x + p.w / 2, p.y - 4))
            mx = (q.x + q.w + p.x) / 2
            self.stars.append(Star(mx, max(3, min(q.y, p.y) - 5)))

    def _decorations(self):
        self.deco = {}      # world column -> [(row, char, colour)]

        def decorate(above, below, c0, c1, dens):
            for c in range(c0, c1):
                bio = self.biome_at(c)
                r = random.random()
                acc = 0.0
                for p, chars, cols in bio.deco:
                    acc += p * dens
                    if r < acc:
                        self.deco.setdefault(c, []).append(
                            (above, random.choice(chars), random.choice(cols)))
                        break
                if below is not None and random.random() < bio.roots[2]:
                    self.deco.setdefault(c, []).append(
                        (below, random.choice(bio.roots[0]), random.choice(bio.roots[1])))

        for p in self.plats:
            decorate(p.y - 1, p.y + 2, 2 * p.x, 2 * (p.x + p.w), 1.0)
        decorate(self.H - 3, None, 0, 2 * self.Wu, 0.7)

    def _scenery(self):
        W, H = self.W, self.H
        rnd = random.Random(5)
        self.sky = [[(rnd.randrange(W * 3), rnd.randrange(2, H - 6), rnd.choice("·.*+"))
                     for _ in range(W // 2)] for _ in range(2)]

    # ---- zone lookup ----
    def slot_at(self, c, dither=True):
        """Zone index at world column c; borders are dithered so zones blend."""
        n = sum(1 for b in self.bounds if c >= b)
        if dither:
            for j, b in enumerate(self.bounds):
                d = c - b
                if -6 <= d < 6:
                    h = ((c * 2654435761) >> 11 & 1023) / 1024.0
                    return j + 1 if h < (d + 6) / 12.0 else j
        return n

    def biome_at(self, c, dither=True):
        return self.zones[self.slot_at(c, dither)]
