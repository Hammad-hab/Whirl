"""Things drawn on the shared sub-cell canvas (pickups, ambient, particles, rocket)."""
import math

from ..colors import cp
from ..gfx.sprites import paint_rocket, star_dots


def pickups(f):
    W, cam, frame = f.W, f.cam, f.game.frame
    for i, st in enumerate(f.level.stars):
        cx = int(st.x * 4) - cam * 2
        if st.got or not -12 < cx < W * 2 + 12:
            continue
        bob = math.sin(frame * 0.2 + i) * 0.6
        star_dots(f.cv, cx, int((st.y + bob) * 4), 3 + int(round(math.sin(frame * 0.25 + i) + 1)))


def ambient(f):
    W, cam = f.W, f.cam
    for a in f.level.ambient:
        cx = int(a.x * 4) - cam * 2
        if not -4 < cx < W * 2 + 4:
            continue
        a.draw(f.cv, cx, int(a.y * 4), f.game.frame)


def particles(f):
    f.game.particles.draw(f.cv, f.cam)


def rocket(f):
    if f.game.status == "flying":
        paint_rocket(f.cv, f.game.rocket, f.cam)


def blit(f):
    f.cv.blit(f.s)


def texts(f):
    f.game.texts.draw(f.s, f.cam)
