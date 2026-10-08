"""Side-scrolling camera (units: columns)."""


class Camera:
    def __init__(self, W):
        self.W = W
        self.x = 0.0

    def snap(self, rocket, level_w):
        self.x = max(0.0, min(2 * rocket.x - self.W * 0.45, 2 * level_w - self.W))

    def follow(self, rocket, level_w):
        """Gentle look-ahead, and the rocket is never allowed off-screen."""
        look = max(-14.0, min(14.0, rocket.vx))
        target = 2 * rocket.x - self.W * 0.45 + look
        self.x += (target - self.x) * 0.15
        sx = 2 * rocket.x - self.x
        lo, hi = self.W * 0.25, self.W * 0.65
        if sx < lo:
            self.x = 2 * rocket.x - lo
        elif sx > hi:
            self.x = 2 * rocket.x - hi
        self.x = max(0.0, min(self.x, 2 * level_w - self.W))
