"""Key bindings and actions. Add a key -> bind(); add behaviour -> @action."""
import curses

from .gfx.canvas import STYLE

BINDINGS = {}     # key code -> action name
ACTIONS = {}      # action name -> fn(game)


def bind(name, *keys):
    for k in keys:
        BINDINGS[k] = name


def action(name):
    def deco(fn):
        ACTIONS[name] = fn
        return fn
    return deco


# lifecycle actions are handled by app.py; the rest are in ACTIONS below
bind("quit", ord("q"), ord("Q"), 27)
bind("restart", ord("r"), ord("R"))
bind("glyphs", ord("b"), ord("B"))
bind("latch", ord("e"), ord("E"))
bind("thrust", ord(" "))
bind("left", curses.KEY_LEFT, ord(","), ord("<"), ord("a"), ord("A"))
bind("right", curses.KEY_RIGHT, ord("."), ord(">"), ord("d"), ord("D"))


@action("glyphs")
def _glyphs(game):
    STYLE["blocks"] = not STYLE["blocks"]


@action("latch")
def _latch(game):
    game.started = True
    game.rocket.toggle_latch()


@action("thrust")
def _thrust(game):
    game.started = True
    game.rocket.press_thrust()


@action("left")
def _left(game):
    game.started = True
    game.rocket.press_left()


@action("right")
def _right(game):
    game.started = True
    game.rocket.press_right()


def poll(stdscr):
    """Drain pending keys; return the list of bound action names."""
    out = []
    while True:
        k = stdscr.getch()
        if k == -1:
            return out
        name = BINDINGS.get(k)
        if name:
            out.append(name)


def dispatch(name, game):
    fn = ACTIONS.get(name)
    if fn:
        fn(game)
