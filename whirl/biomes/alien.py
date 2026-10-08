from ..colors import C, CYN, LIME, MAG
from .base import Biome, register


@register
def build():
    c = C
    return Biome(
        name="ALIEN", note="low gravity", accent=MAG,
        haze=(c(53), c(30)), hb=0.05,
        explodeOnContact=False,
        grass=(c(54), c(91), c(128), c(171)), dirt=(c(17), c(54)),
        mount=(c(17), c(55)), shape="spike", hedge=c(54),
        stars=True, sky="planet", skyc=(c(99), c(141), c(51)),
        deco=[(0.07, "◆", (c(51), c(201), c(154))), (0.20, "',`", (c(51), c(201))),
              (0.05, "○", (c(154), c(226)))],
        roots=("╷▾", (c(51), c(201)), 0.12),
        grav=0.2, fric=0.85, fx="spore", fxn=0.20, fxc=(CYN, MAG, LIME))
