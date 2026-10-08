from ..colors import (BR2, BRN, CYN, G1, G2, G3, G4, GREENS, GRN, GRY, HZ1, HZ2, BLU, FAR,
                      LIME, MAG, ORG, PALE, RED, YEL)
from .base import Biome, register


@register
def build():
    return Biome(
        name="MEADOW", note="", accent=GRN,
        haze=(HZ1, HZ2), hb=0.0,
        grass=GREENS, dirt=(BRN, BR2), mount=(FAR, BLU), shape="round", hedge=G1,
        stars=True, sky="moon", skyc=(PALE, GRY, HZ2),
        deco=[(0.07, "♣", (G1, G2)), (0.23, "',`", (G3, G4)),
              (0.04, "•", (RED, YEL, MAG, ORG, CYN))],
        roots=("▾╷", (BRN, BR2), 0.10),
        explodeOnContact=False,
        grav=1.0, fric=0.85, fx="firefly", fxn=0.12, fxc=(LIME,))
