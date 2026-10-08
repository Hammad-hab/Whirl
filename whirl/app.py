"""Entry point: terminal setup, argument parsing and the fixed-timestep main loop."""
import argparse
import curses
import locale
import time

from . import biomes, input as keys
from .colors import init_colors
from .config import DT, MIN_H, MIN_W
from .game import Game
from .gfx.canvas import STYLE
from .render.renderer import Renderer


def parse_args(argv=None):
    p = argparse.ArgumentParser(prog="rocket", description="ASCII rocket platformer")
    p.add_argument("--biome", help="force a biome (meadow|desert|tundra|volcano|alien); default random")
    p.add_argument("--blocks", action="store_true", help="use block glyphs instead of Braille")
    return p.parse_args(argv)


def main(stdscr, opts):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    init_colors()
    biomes.load()
    STYLE["blocks"] = opts.blocks
    H, W = stdscr.getmaxyx()
    if H < MIN_H or W < MIN_W:
        raise SystemExit(f"Terminal too small (need at least {MIN_W}x{MIN_H})")

    def new_game():
        return Game(W, H, biomes.pick(opts.biome))

    game = new_game()
    renderer = Renderer()
    while True:
        t0 = time.time()
        for name in keys.poll(stdscr):
            if name == "quit":
                return
            if name == "restart":
                game = new_game()
                continue
            keys.dispatch(name, game)
        game.update()
        renderer.draw(stdscr, game)
        rem = DT - (time.time() - t0)
        if rem > 0:
            time.sleep(rem)


def run(argv=None):
    opts = parse_args(argv)
    locale.setlocale(locale.LC_ALL, "")
    try:
        curses.wrapper(main, opts)
    except KeyboardInterrupt:
        pass
