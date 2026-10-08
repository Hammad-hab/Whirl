import random

from ..gfx.canvas import Canvas


class Frame:
    """Everything a render layer needs for one frame."""

    def __init__(self, s, game):
        self.s = s
        self.game = game
        self.level = game.level
        self.W, self.H = game.W, game.H
        cam = int(round(game.camera.x))
        if game.shake > 0:
            cam += random.randint(-2, 2)
        self.cam = cam
        # zone index + biome for every screen column (dithered at borders so zones blend)
        self.slots = [self.level.slot_at(col + cam) for col in range(self.W)]
        self.bb = [self.level.zones[i] for i in self.slots]
        self.cv = Canvas()      # sub-cell layer shared by pickups / particles / rocket
