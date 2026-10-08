"""Tiny publish/subscribe bus so features can react to game events without editing core code.

Built-in events (emitted by Game / systems):
    star(star)   crash()   win()   biome_enter(biome)
Handlers are called as fn(game, **info).
"""
from collections import defaultdict


class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)

    def on(self, name, fn=None):
        """Register fn for an event; also usable as a decorator: @bus.on("crash")."""
        if fn is None:
            return lambda f: self.on(name, f)
        self._handlers[name].append(fn)
        return fn

    def emit(self, name, game, **info):
        for fn in self._handlers[name]:
            fn(game, **info)
