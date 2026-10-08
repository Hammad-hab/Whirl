from ..colors import C, YEL
from .base import Biome, register


@register
def build():
    c = C
    return Biome(
        name="DESERT", note="hot and dry", accent=YEL,
        haze=(c(130), c(172)), hb=0.05,
        grass=(c(136), c(178), c(214), c(221)), dirt=(c(137), c(173)),
        mount=(c(95), c(131)), shape="mesa", hedge=c(130),
        stars=False, sky="sun", skyc=(c(226), c(255), c(208)),
        deco=[(0.04, "Ψψ", (c(28), c(34))), (0.18, "·.,", (c(180), c(222), c(137))),
              (0.03, "•", (c(205), c(226)))],
        roots=("╷ı", (c(137), c(95)), 0.07),
        grav=1.0, fric=0.85, fx="dust", fxn=0.20, fxc=(c(222), c(180)))
