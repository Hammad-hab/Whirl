from ..colors import C, CYN, GRY, WHT
from .base import Biome, register


@register
def build():
    c = C
    return Biome(
        name="TUNDRA", note="icy - you'll slide!", accent=CYN,
        haze=(c(24), c(67)), hb=-0.1,
        grass=(c(110), c(153), c(195), c(231)), dirt=(c(67), c(60)),
        mount=(c(60), c(110)), shape="peak", hedge=c(24),
        stars=True, sky="aurora", skyc=(WHT, GRY, CYN),
        deco=[(0.07, "♠", (c(22), c(29), c(255))), (0.20, "*.'", (c(255), c(153))),
              (0.03, "•", (c(81), c(159)))],
        roots=("╿▼", (c(117), c(153)), 0.14),
        grav=1.0, fric=0.97, fx="snow", fxn=0.35, fxc=(WHT,))
