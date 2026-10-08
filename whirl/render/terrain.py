"""Platforms, ground, decorations and the goal flag."""
from ..colors import DARK, RED, WHT, YEL, cp
from ..gfx.term import put


def platforms(f):
    s, W, cam, bb = f.s, f.W, f.cam, f.bb
    for px, py, pw in f.level.plats:
        c0, c1 = int(2 * px), int(2 * (px + pw))
        for c in range(max(c0, cam), min(c1, cam + W)):
            b = bb[c - cam]
            gi = (c * 7 + (c // 3) * 5) % 4
            put(s, py, c - cam, "▀", cp(b.grass[gi], gi >= 2))
            put(s, py + 1, c - cam, "▓" if c % 5 else "▒", cp(b.dirt[0] if c % 3 else b.dirt[1]))


def ground(f):
    s, H, cam = f.s, f.H, f.cam
    for col in range(f.W - 1):
        c = col + cam
        b = f.bb[col]
        gi = (c * 7 + (c // 3) * 5) % 4
        put(s, H - 2, col, "▀", cp(b.grass[gi], gi >= 2))
        put(s, H - 1, col, "▒" if c % 4 else "░", cp(b.dirt[0] if c % 2 else b.dirt[1]))


def decorations(f):
    deco = f.level.deco
    for col in range(f.W):
        for row, ch, color in deco.get(col + f.cam, ()):
            put(f.s, row, col, ch, cp(color, color not in DARK))


def flag(f):
    s = f.s
    gx, gy = f.level.goal
    gc = int(2 * gx) - f.cam
    for k in range(1, 5):
        put(s, gy - k, gc, "┃", cp(WHT, True))
    put(s, gy - 4, gc + 1, "▶▶" if (f.game.frame // 6) % 2 else "▶ ", cp(RED, True))
    put(s, gy - 5, gc - 2, "GOAL", cp(YEL, True))
