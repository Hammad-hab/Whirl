"""Colour ids, lazy 256-colour pair registration and curses attribute helpers."""
import curses

(RED, YEL, WHT, CYN, GRN, MAG, BLU, ORG, GRY, BRN, FAR,
 G1, G2, G3, G4, BR2, PALE, HZ1, HZ2, LIME) = range(1, 21)
GREENS = (G1, G2, G3, G4)
CONFETTI = (RED, YEL, CYN, MAG, GRN, ORG, WHT)

HI = [True]           # 256-colour terminal?
_PAIRS = {}
DARK = set()          # colours drawn without bold (filled by biomes.load)


def basic_of(n):
    """Rough 8-colour fallback for a 256-colour number."""
    if n < 16:
        return n % 8
    if n >= 232:
        return 7 if n > 243 else 0
    n -= 16
    r, g, b = n // 36, n // 6 % 6, n % 6
    bits = (r >= 3) | ((g >= 3) << 1) | ((b >= 3) << 2)
    return bits or 7


def C(n):
    """Lazily register a colour pair for 256-colour number n; returns the pair id."""
    if n in _PAIRS:
        return _PAIRS[n]
    idx = 30 + len(_PAIRS)
    try:
        curses.init_pair(idx, n if HI[0] else basic_of(n), -1)
    except curses.error:
        idx = WHT
    _PAIRS[n] = idx
    return idx


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    hi = curses.COLORS >= 256
    HI[0] = hi
    c = curses
    table = {
        RED: (196, c.COLOR_RED), YEL: (226, c.COLOR_YELLOW), WHT: (15, c.COLOR_WHITE),
        CYN: (51, c.COLOR_CYAN), GRN: (46, c.COLOR_GREEN), MAG: (201, c.COLOR_MAGENTA),
        BLU: (19, c.COLOR_BLUE), ORG: (208, c.COLOR_YELLOW), GRY: (245, c.COLOR_WHITE),
        BRN: (94, c.COLOR_RED), FAR: (18, c.COLOR_BLUE),
        G1: (22, c.COLOR_GREEN), G2: (28, c.COLOR_GREEN), G3: (34, c.COLOR_GREEN),
        G4: (41, c.COLOR_GREEN), BR2: (130, c.COLOR_YELLOW), PALE: (230, c.COLOR_WHITE),
        HZ1: (53, c.COLOR_MAGENTA), HZ2: (90, c.COLOR_MAGENTA), LIME: (154, c.COLOR_GREEN),
    }
    for i, (rich, basic) in table.items():
        curses.init_pair(i, rich if hi else basic, -1)


def cp(n, bold=False):
    return curses.color_pair(n) | (curses.A_BOLD if bold else 0)
