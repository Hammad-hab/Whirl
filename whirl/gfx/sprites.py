"""Pixel-ish sprites: the rocket and the collectible star."""
import math
import random

from ..colors import CYN, GRY, ORG, RED, WHT, YEL


def star_dots(cv, cx, cy, arm):
    cv.dot(cx, cy, WHT)
    for k in range(1, arm + 1):
        c = YEL if k < arm else ORG
        cv.dot(cx + k, cy, c)
        cv.dot(cx - k, cy, c)
        cv.dot(cx, cy + k, c)
        cv.dot(cx, cy - k, c)
    for k in range(1, arm // 2 + 1):
        for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            cv.dot(cx + sx * k, cy + sy * k, ORG)


def rocket_shape(t, a, L, rnd):
    """Rocket in local coords (t along the axis, a = |sideways|). Returns colour or 0."""
    if t > 1.85 or t < -1.5 - L:
        return 0
    if t > 0.85:                                    # nose cone
        w = 0.72 * (1 - (t - 0.85)) ** 0.6
        return RED if a <= w else 0
    if t >= -1.15:                                  # body + fins
        if a <= 0.72:
            if (t - 0.3) ** 2 + a * a <= 0.13:
                return CYN
            if -0.55 <= t <= -0.4:
                return RED
            return WHT
        if t < -0.25 and a <= 0.72 + 0.85 * (-0.25 - t) / 1.1:
            return RED
        return 0
    if t >= -1.5:                                   # nozzle
        if a <= 0.42:
            return GRY
        if t >= -1.35 and a <= 0.72 + 0.85 * (-0.25 - t) / 1.1:
            return RED
        return 0
    d = -1.5 - t                                    # flame
    if L <= 0 or d > L:
        return 0
    w = 0.42 * (1 - d / L) ** 0.7 * (0.8 + 0.4 * rnd())
    if a > w:
        return 0
    f = d / L
    return WHT if f < 0.2 else YEL if f < 0.45 else ORG if f < 0.7 else RED


def paint_rocket(cv, rocket, cam):
    sn, cs = math.sin(rocket.th), math.cos(rocket.th)
    ox = cam * 2
    L = random.uniform(1.7, 2.6) if rocket.thrusting else 0.0
    rnd = random.random
    x0, y0 = int(rocket.x * 4) - 17, int(rocket.y * 4) - 17
    for dy in range(y0, y0 + 35):
        ry = (dy + 0.5) / 4 - rocket.y
        for dx in range(x0, x0 + 35):
            rx = (dx + 0.5) / 4 - rocket.x
            t = rx * sn - ry * cs
            p = rx * cs + ry * sn
            col = rocket_shape(t, abs(p), L, rnd)
            if col:
                cv.dot(dx - ox, dy, col)
    # little side-thruster puffs while rotating
    side = 1 if (rocket.rt > 0 and rocket.lt <= 0) else -1 if (rocket.lt > 0 and rocket.rt <= 0) else 0
    if side:
        for t, p in ((1.2, -side), (-1.2, side)):
            for k in range(3):
                pp = p * (1.0 + 0.3 * k)
                ux = rocket.x + t * sn + pp * cs
                uy = rocket.y - t * cs + pp * sn
                cv.dot(int(ux * 4) - ox, int(uy * 4), YEL)
