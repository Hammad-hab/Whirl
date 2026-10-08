"""Background mountain profiles. Add one with @shape("name"), then set `shape="name"` on a Biome."""
import math

SHAPES = {}     # name -> fn(world_col, base, amp, seed) -> height in rows


def shape(name):
    def deco(fn):
        SHAPES[name] = fn
        return fn
    return deco


def _rolling(wc, seed):
    return (0.6 * math.sin(wc * 0.03 + seed) + 0.3 * math.sin(wc * 0.10 + seed * 2)
            + 0.1 * math.sin(wc * 0.23 + seed * 3))


def _ridged(wc, seed, k):
    return (1 - abs(math.sin(wc * k + seed))) * 1.6 - 0.8 + 0.15 * math.sin(wc * 0.21 + seed * 3)


@shape("round")
def round_hills(wc, base, amp, seed):
    return base + amp * _rolling(wc, seed)


@shape("mesa")
def mesa(wc, base, amp, seed):
    return base + amp * round(_rolling(wc, seed) * 3) / 3


@shape("peak")
def peak(wc, base, amp, seed):
    return base + amp * 1.4 * _ridged(wc, seed, 0.04)


@shape("spike")
def spike(wc, base, amp, seed):
    return base + amp * 1.4 * _ridged(wc, seed, 0.09)


def height(name, wc, base, amp, seed):
    return SHAPES[name](wc, base, amp, seed)
