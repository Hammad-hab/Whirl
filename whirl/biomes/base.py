"""Biome definition + registry.

A biome is just data. To add one: copy a file in this folder, tweak it, and import it in
biomes/__init__.py. Builders run AFTER curses colours are ready, so C(n) is safe inside them.
"""
from dataclasses import dataclass, field

_BUILDERS = []


@dataclass(eq=False)
class Biome:
    name: str
    accent: int
    explodeOnContact: bool
    haze: tuple            # (upper, lower) haze colours
    grass: tuple           # 4 colours for the platform top
    dirt: tuple            # 2 colours for the platform body
    mount: tuple           # colours for (far, near) mountain layers
    hedge: int
    skyc: tuple            # (main, alt, halo) for the sky body
    deco: list             # [(chance, "chars", (colours...)), ...] drawn on top of platforms
    roots: tuple           # (chars, colours, chance) drawn under platforms
    note: str = ""         # subtitle shown on the entry banner
    hb: float = 0.0        # haze bias
    shape: str = "round"   # key in gfx.mountain_shapes.SHAPES
    stars: bool = True     # twinkling background stars?
    sky: str = "moon"      # key in gfx.sky.BODIES / OVERLAYS
    grav: float = 1.0      # gravity multiplier
    fric: float = 0.85     # ground friction (closer to 1 = slippery)
    fx: str = ""           # key in effects.EFFECTS (ambient particles)
    fxn: float = 0.0       # ambient density (per unit of level width)
    fxc: tuple = ()        # ambient colours
    props: dict = field(default_factory=dict)   # free-form slot for new mechanics (e.g. {"heat": 2.0})


def register(fn):
    """Decorator: register a zero-arg function returning a Biome."""
    _BUILDERS.append(fn)
    return fn


def build_all():
    return [b() for b in _BUILDERS]
