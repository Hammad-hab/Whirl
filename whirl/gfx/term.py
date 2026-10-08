import curses


def put(s, y, x, text, attr=0):
    """Clipped addstr that never raises."""
    h, w = s.getmaxyx()
    if 0 <= y < h and 0 <= x < w and text:
        try:
            s.addstr(y, x, text[: w - x], attr)
        except curses.error:
            pass
