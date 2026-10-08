"""Sky, stars, mountains, horizon."""
from ..colors import GRY, WHT, cp
from ..gfx.canvas import BIT, Canvas, tochar
from ..gfx.mountain_shapes import height
from ..gfx.sky import BODIES, OVERLAYS
from ..gfx.term import put

MOUNTAIN_LAYERS = [   # (parallax, colour index in biome.mount, base, amp, seed)
    (0.18, 0, 6, 3, 1.0),
    (0.40, 1, 3.5, 2.5, 4.0),
]


def haze(f):
    """Haze above the horizon (ordered dither), drawn in runs of equal biome."""
    s, W, H, bb = f.s, f.W, f.H, f.bb
    top = H - 17
    thr = (0.0, 0.5, 0.25, 0.75)
    c0 = 0
    while c0 < W:
        c1 = c0 + 1
        while c1 < W and bb[c1] is bb[c0]:
            c1 += 1
        b = bb[c0]
        for r in range(top, H - 2):
            k = max(0.0, min(1.0, (r - top) / (H - 3 - top) + b.hb))
            row = "".join(
                (("▒" if k > 0.7 else "░") if k > thr[(c + (r & 1) * 2) % 4] else " ")
                for c in range(c0, c1))
            put(s, r, c0, row, cp(b.haze[0] if k < 0.55 else b.haze[1]))
        c0 = c1


def overlays(f):
    for col in range(f.W):
        fn = OVERLAYS.get(f.bb[col].sky)
        if fn:
            fn(f.s, col, col + f.cam, f.game.frame)


def sky_bodies(f):
    """Moon / sun / planet, clipped to their own biome zone."""
    W, cam = f.W, f.cam
    for i, b in enumerate(f.level.zones):
        paint = BODIES.get(b.sky)
        if paint is None:
            continue
        mx = int((W * 0.62 + (f.level.centers[i] - cam) * 0.08) * 2)
        if not -40 < mx < W * 2 + 40:
            continue
        mc = Canvas()
        paint(mc, b.skyc, mx, 26)
        mc.blit(f.s, lambda col, i=i: 0 <= col < W and f.slots[col] == i)


def starfield(f):
    for layer, fac in enumerate((0.08, 0.2)):
        for i, (sx, sy, ch) in enumerate(f.level.sky[layer]):
            col = (sx - int(f.cam * fac)) % f.W
            if not f.bb[col].stars:
                continue
            bright = (f.game.frame // 12 + i) % 11 == 0
            put(f.s, sy, col, ch, cp(WHT if bright else GRY))


def _mountain_layer(f, fac, layer, base, amp, seed):
    s, W, H, cam, bb = f.s, f.W, f.H, f.cam, f.bb
    base_y = (H - 3) * 4
    for col in range(W):
        b = bb[col]
        hs = []
        for sub in (0, 1):
            wc = (col * 2 + sub + int(cam * 2 * fac)) / 2.0
            hs.append(base_y - int(height(b.shape, wc, base, amp, seed) * 4))
        top = max(hs)
        color = b.mount[layer]
        for r in range(min(hs) >> 2, H - 3):
            if r * 4 >= top:
                mask = 0xFF
            else:
                mask = 0
                for sub in (0, 1):
                    for dy in range(4):
                        if hs[sub] <= r * 4 + dy < base_y:
                            mask |= BIT[sub][dy]
            if mask:
                put(s, r, col, "█" if mask == 0xFF else tochar(mask), cp(color))


def mountains(f):
    for args in MOUNTAIN_LAYERS:
        _mountain_layer(f, *args)


def hedge(f):
    """Dark hedge line along the horizon."""
    for col in range(f.W - 1):
        c = col + f.cam
        put(f.s, f.H - 3, col, "▃▄▅"[(c * 5 + c // 4) % 3], cp(f.bb[col].hedge))
