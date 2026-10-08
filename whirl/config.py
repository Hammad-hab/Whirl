"""Tunable constants. Change the feel of the game here, nowhere else."""

FPS = 30
DT = 1 / FPS

# ---- physics ----
GRAVITY = 8.0              # lower = floatier (biomes multiply this)
THRUST = 21.0
TURN = 3.0                 # rad/s while a rotate key is held
MAX_V = 22.0
DRAG = 0.25
R = 1.5                    # collision radius
CRASH_V = 20.0             # impact speed that always crashes
SOFT_CRASH_V = 11.0        # ...or this fast while tilted more than...
SOFT_CRASH_ANGLE = 1.2     # ...this many radians
CRASH_TIME = 1.4           # seconds before respawn
SHAKE_FRAMES = 12

# ---- boost ----
BOOST_MAX = 100.0
BOOST_DRAIN = 9.0          # per second while thrusting
BOOST_REGEN_GROUND = 45.0  # per second when touching ground
BOOST_REGEN_AIR = 4.0      # per second when coasting

# ---- input: frames a key press counts as "held" (terminals only send repeats) ----
THRUST_HOLD = 9
TURN_HOLD = 6

# ---- terminal ----
MIN_W = 60
MIN_H = 24

# ---- level generation (units: 1 row = 1 u, 1 u = 2 columns) ----
NUM_PLATFORMS = 14
START_PLATFORM_W = 14
PLATFORM_GAP = (5, 10)
PLATFORM_W = (9, 15)
PLATFORM_DY = 7
LEVEL_TAIL = 25
