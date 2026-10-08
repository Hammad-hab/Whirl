"""Sky bodies (drawn on a Canvas) and per-column sky overlays (e.g. aurora).

Add one:   @body("comet") def comet(cv, colors, mx, my): ...
then set `sky="comet"` on a Biome. Overlays work the same via @overlay.
"""
import math

from ..colors import CYN, GRN, MAG, cp
from .term import put

BODIES = {}      # name -> fn(cv, (main, alt, halo), mx, my)
OVERLAYS = {}    # name -> fn(screen, col, world_col, frame)


def body(name):
    def deco(fn):
        BODIES[name] = fn
        return fn
    return deco


def overlay(name):
    def deco(fn):
        OVERLAYS[name] = fn
        return fn
    return deco


@body("moon")
def moon(cv, colors, mx, my):
    main, alt, halo = colors
    r0 = 9
    for dy in range(-r0 - 4, r0 + 5):
        for dx in range(-r0 - 4, r0 + 5):
            d2 = dx * dx + dy * dy
            if d2 <= r0 * r0:
                crater = ((dx + 3) ** 2 + (dy - 2) ** 2 <= 6 or (dx - 4) ** 2 + (dy + 4) ** 2 <= 4
                          or (dx - 2) ** 2 + (dy - 6) ** 2 <= 3)
                cv.dot(mx + dx, my + dy, alt if crater else main)
            elif d2 <= (r0 + 3) ** 2 and (dx + dy) % 3 == 0:
                cv.dot(mx + dx, my + dy, halo)


@body("sun")
def sun(cv, colors, mx, my):
    main, alt, halo = colors
    r0 = 10
    for dy in range(-r0 - 5, r0 + 6):
        for dx in range(-r0 - 5, r0 + 6):
            d2 = dx * dx + dy * dy
            if d2 <= r0 * r0:
                cv.dot(mx + dx, my + dy, alt if d2 <= (0.55 * r0) ** 2 else main)
            elif d2 <= (r0 + 4) ** 2 and (dx + dy) % 3 == 0:
                cv.dot(mx + dx, my + dy, halo)


@body("planet")
def planet(cv, colors, mx, my):
    main, alt, halo = colors
    r0 = 8
    for dy in range(-r0, r0 + 1):
        for dx in range(-r0, r0 + 1):
            if dx * dx + dy * dy <= r0 * r0:
                cv.dot(mx + dx, my + dy, alt if ((dy + r0) // 3) % 2 == 0 else main)
    for k in range(180):
        a = k * 2 * math.pi / 180
        x = int(1.9 * r0 * math.cos(a))
        y = int(0.35 * r0 * math.sin(a) - x * 0.18)
        if math.sin(a) < 0 and x * x + y * y <= r0 * r0:
            continue                      # back half of the ring hides behind the planet
        cv.dot(mx + x, my + y, halo)


@overlay("aurora")
def aurora(s, col, wc, frame):
    base = 3 + 2 * math.sin(wc * 0.06 + frame * 0.04)
    for j in range(4):
        colr = (GRN, CYN, MAG)[(wc // 18 + j // 2) % 3]
        put(s, int(base) + j, col, "▒" if j in (1, 2) else "░", cp(colr))
