"""Ordered list of render layers. Insert yours with Renderer.add_layer(name, fn, before="blit")."""
from . import background, entities, hud, terrain
from .frame import Frame


class Renderer:
    def __init__(self):
        self.layers = [
            ("haze", background.haze),
            ("overlays", background.overlays),
            ("sky_bodies", background.sky_bodies),
            ("starfield", background.starfield),
            ("mountains", background.mountains),
            ("hedge", background.hedge),
            ("platforms", terrain.platforms),
            ("ground", terrain.ground),
            ("decorations", terrain.decorations),
            ("flag", terrain.flag),
            # -- sub-cell canvas layers, flushed together by "blit" --
            ("pickups", entities.pickups),
            ("ambient", entities.ambient),
            ("particles", entities.particles),
            ("rocket", entities.rocket),
            ("blit", entities.blit),
            ("texts", entities.texts),
            ("hud", hud.hud),
            ("banners", hud.banners),
        ]

    def add_layer(self, name, fn, before=None, after=None):
        names = [n for n, _ in self.layers]
        if before is not None:
            i = names.index(before)
        elif after is not None:
            i = names.index(after) + 1
        else:
            i = len(self.layers)
        self.layers.insert(i, (name, fn))

    def draw(self, s, game):
        s.erase()
        f = Frame(s, game)
        for _, fn in self.layers:
            fn(f)
        s.refresh()
