"""Sub-cell graphics: Braille gives a 2x4 dot grid inside every character."""
from ..colors import cp
from .term import put

BIT = ((0x01, 0x02, 0x04, 0x40), (0x08, 0x10, 0x20, 0x80))

# Some terminals/fonts draw Braille with gaps. Block mode folds the same 2x4 dots into
# 2x2 quadrant blocks, which terminals draw as solid shapes.
QUAD = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
_QUAD_OF = [(1 if b & 0x03 else 0) | (2 if b & 0x18 else 0) | (4 if b & 0x44 else 0) | (8 if b & 0xA0 else 0)
            for b in range(256)]
STYLE = {"blocks": False}


def tochar(bits):
    return QUAD[_QUAD_OF[bits]] if STYLE["blocks"] else chr(0x2800 + bits)


class Canvas:
    """Collects dots in (x, y) sub-cell coordinates, then blits them as glyphs."""

    def __init__(self):
        self.cells = {}

    def dot(self, x, y, col):
        key = (y >> 2, x >> 1)
        e = self.cells.get(key)
        if e is None:
            e = self.cells[key] = [0, {}]
        e[0] |= BIT[x & 1][y & 3]
        e[1][col] = e[1].get(col, 0) + 1

    def blit(self, s, keep=None):
        for (r, c), (bits, cols) in self.cells.items():
            if keep is not None and not keep(c):
                continue
            put(s, r, c, tochar(bits), cp(max(cols, key=cols.get), True))
