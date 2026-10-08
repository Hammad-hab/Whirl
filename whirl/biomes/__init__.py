import random

from ..colors import DARK
from .base import Biome, build_all, register  # noqa: F401

# Import order = registration order. Add new biome modules here.
from . import meadow, desert, tundra, volcano, alien  # noqa: F401,E402

BIOMES = []


def load():
    """Build every registered biome (call once, after curses colours are initialised)."""
    BIOMES[:] = build_all()
    for b in BIOMES:
        DARK.update(b.grass[:2])
        DARK.update(b.roots[1])


def pick(name=None):
    """Biome by (case-insensitive) name, or a random one."""
    if name:
        for b in BIOMES:
            if b.name.lower() == name.lower():
                return b
    return random.choice(BIOMES)
