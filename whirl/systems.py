"""Per-frame gameplay rules. A System is anything with update(game).

Game.flying_systems run only while the rocket is flying (and didn't crash this frame).
Game.systems run every frame. To add a mechanic (heat, fuel pickups, wind...), write a
System and append it to one of those lists in Game.__init__.
"""
from .config import (BOOST_MAX, BOOST_REGEN_AIR, BOOST_REGEN_GROUND, DT, R)


class System:
    def update(self, game):
        raise NotImplementedError


class GroundContact(System):
    """Friction, levelling out, checkpoint saving and boost recharge."""

    def update(self, game):
        r, bio = game.rocket, game.biome
        if game.grounded:
            r.vx *= bio.fric
            if not (r.lt or r.rt):
                r.th -= r.th * min(1.0, 5 * DT)
                r.om = 0.0
            if abs(r.vx) < 2.5 and abs(r.vy) < 2:
                r.checkpoint = (r.x, r.y)
            r.boost += BOOST_REGEN_GROUND * DT
        elif not r.thrusting:
            r.boost += BOOST_REGEN_AIR * DT
        r.boost = max(0.0, min(BOOST_MAX, r.boost))


class StarCollector(System):
    def update(self, game):
        r = game.rocket
        for st in game.level.stars:
            if not st.got and (r.x - st.x) ** 2 + (r.y - st.y) ** 2 < (R + 1.4) ** 2:
                st.got = True
                game.got += 1
                game.emit("star", star=st)


class GoalWatcher(System):
    def update(self, game):
        gx, gy = game.level.goal
        r = game.rocket
        if not game.won and abs(r.x - gx) < 3 and abs(r.y - (gy - 3)) < 4:
            game.won = True
            game.emit("win")


class WinConfetti(System):
    def update(self, game):
        if game.won and game.frame % 5 == 0:
            game.particles.confetti(game.level.goal[0])


class AmbientFx(System):
    def update(self, game):
        for a in game.level.ambient:
            a.update(game.frame, game.H)
