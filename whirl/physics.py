"""Collision handling (circle vs. axis-aligned rectangles) and world bounds."""
import math

from .config import CRASH_V, R, SOFT_CRASH_ANGLE, SOFT_CRASH_V


def resolve(rocket, solids, particles):
    """Push the rocket out of solids and bounce it. Returns (grounded, crashed)."""
    grounded = False
    for rx, ry, rw, rh in solids:
        if rocket.x < rx - R - 1 or rocket.x > rx + rw + R + 1:
            continue
        nx = min(max(rocket.x, rx), rx + rw)
        ny = min(max(rocket.y, ry), ry + rh)
        dx, dy = rocket.x - nx, rocket.y - ny
        d2 = dx * dx + dy * dy
        if d2 >= R * R:
            continue
            
        if d2 > 1e-9:
            d = math.sqrt(d2)
            gx, gy = dx / d, dy / d
            rocket.x += gx * (R - d)
            rocket.y += gy * (R - d)
        else:
            gx, gy = 0.0, -1.0
            rocket.y = ry - R
        vn = rocket.vx * gx + rocket.vy * gy
        if vn < 0:
            impact = -vn
       
            top = gy < -0.6
            if top and (impact > CRASH_V or (impact > SOFT_CRASH_V and abs(rocket.th) > SOFT_CRASH_ANGLE)):
                return grounded, True
                
            e = 0.2 if impact > 6 else 0.0
            rocket.vx -= (1 + e) * vn * gx
            rocket.vy -= (1 + e) * vn * gy
            if top and impact > 4:
                particles.landing_puff(rocket)
        
        if gy < -0.6:
            grounded = True

    if rocket.bio.explodeOnContact and grounded:
         return grounded, True
         
    return grounded, False


def clamp_to_world(rocket, level_w):
    if rocket.x < R or rocket.x > level_w - R:
        rocket.x = max(R, min(level_w - R, rocket.x))
        rocket.vx = 0.0
    if rocket.y < R:
        rocket.y, rocket.vy = R, max(rocket.vy, 0.0)
