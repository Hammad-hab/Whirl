"""HUD widgets and banners. Add one with @widget / @banner; each is a function f(frame_ctx)."""
from ..colors import CYN, GRN, GRY, RED, WHT, YEL, cp
from ..gfx.term import put

EIGHTHS = " ▏▎▍▌▋▊▉█"
HELP = "SPACE thrust  < > rotate  E latch  B glyphs  R restart  Q quit"

WIDGETS = []
BANNERS = []


def widget(fn):
    WIDGETS.append(fn)
    return fn


def banner(fn):
    BANNERS.append(fn)
    return fn


def hud(f):
    for fn in WIDGETS:
        fn(f)


def banners(f):
    for fn in BANNERS:
        fn(f)


def _centered(f, row, text, attr):
    put(f.s, row, (f.W - len(text)) // 2, text, attr)


# ---------------- widgets ----------------
@widget
def boost_bar(f):
    s, boost = f.s, f.game.rocket.boost
    put(s, 0, 1, "BOOST ", cp(WHT, True))
    for i in range(20):
        fill = max(0.0, min(8.0, boost / 100.0 * 160 - i * 8))
        colr = RED if i < 5 else YEL if i < 10 else GRN
        if fill >= 8:
            put(s, 0, 7 + i, "█", cp(colr, True))
        elif fill > 0:
            put(s, 0, 7 + i, EIGHTHS[int(fill)], cp(colr, True))
        else:
            put(s, 0, 7 + i, "░", cp(GRY))
    put(s, 0, 28, f"{int(boost):3d}%", cp(GRN if boost > 30 else YEL if boost > 10 else RED))


@widget
def star_counter(f):
    put(f.s, 0, 35, f"★ {f.game.got}/{f.game.total_stars}", cp(YEL, True))


@widget
def latch_indicator(f):
    if f.game.rocket.latch:
        put(f.s, 0, 46, "ENGINE LATCHED", cp(CYN, True))


@widget
def biome_name(f):
    b = f.game.biome
    put(f.s, 0, max(0, f.W - len(b.name) - 2), b.name, cp(b.accent, True))


@widget
def out_of_boost(f):
    if f.game.rocket.boost <= 0 and f.game.status == "flying":
        put(f.s, 1, 1, "out of boost - land to recharge", cp(RED, True))


@widget
def help_line(f):
    put(f.s, 1, max(0, f.W - len(HELP) - 1), HELP, cp(GRY))


# ---------------- banners ----------------
@banner
def biome_entry(f):
    g = f.game
    if g.btime > 0 and not g.won:
        _centered(f, f.H // 4, f"~ {g.biome.name} ~", cp(g.biome.accent, True))
        if g.biome.note:
            _centered(f, f.H // 4 + 1, g.biome.note, cp(WHT))


@banner
def intro(f):
    g = f.game
    if not g.started and not g.won:
                                             
        _centered(f, f.H // 3,   "██╗    ██╗██╗  ██╗██╗██████╗ ██╗     ", cp(YEL, True))
        _centered(f, f.H // 3+1, "██║ █╗ ██║███████║██║██████╔╝██║     ", cp(YEL, True))
        _centered(f, f.H // 3+2, "██║███╗██║██╔══██║██║██╔══██╗██║      ", cp(YEL, True))
        _centered(f, f.H // 3+3, "╚███╔███╔╝██║  ██║██║██║  ██║███████╗", cp(YEL, True))
        _centered(f, f.H // 3+4, " ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝", cp(YEL, True))
        _centered(f, f.H // 3 + 5, "fly right, grab the stars, reach the flag  →", cp(WHT))


@banner
def crashed(f):
    if f.game.status == "crashed":
        _centered(f, f.H // 3, "OOPS!  respawning...", cp(RED, True))


@banner
def won(f):
    g = f.game
    if g.won:
        _centered(f, f.H // 3, f"YOU MADE IT!   ★ {g.got}/{g.total_stars}", cp(GRN, True))
        _centered(f, f.H // 3 + 1, "press R to play again", cp(WHT))
