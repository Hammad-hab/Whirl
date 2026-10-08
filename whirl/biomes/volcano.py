from ..colors import C, ORG, RED, YEL
from .base import Biome, register


@register
def build():
    c = C
    return Biome(
        name="VOLCANO", note="heavy gravity", accent=RED,
        haze=(c(52), c(124)), hb=0.15,
        grass=(c(52), c(88), c(160), c(208)), dirt=(c(236), c(239)),
        mount=(c(52), c(88)), shape="peak", hedge=c(52),
        stars=False, sky="moon", skyc=(c(160), c(88), c(124)),
        deco=[(0.06, "▲", (c(239), c(242))), (0.20, "^'", (c(202), c(208), c(160))),
              (0.04, "•", (c(226), c(208)))],
        roots=("▾╷", (c(202), c(160)), 0.12),
        grav=1.15, fric=0.85, fx="ember", fxn=0.30, fxc=(ORG, RED, YEL))
