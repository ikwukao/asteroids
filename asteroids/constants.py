"""
Global game configuration.

This module centralizes the game's configurable values, including screen
dimensions, player settings, asteroid behavior, and projectile properties.

Keeping these values in a single location makes the game easier to tune,
maintain, and balance without modifying gameplay logic.
"""

# ---------------------------------------------------------------------------
# Display Configuration
# ---------------------------------------------------------------------------

# Dimensions of the game window in pixels.
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# ---------------------------------------------------------------------------
# Player Configuration
# ---------------------------------------------------------------------------

# Collision radius of the player's ship.
PLAYER_RADIUS = 20

# Width of the outlines used when rendering game objects.
LINE_WIDTH = 2

# Rotation speed of the player in degrees per second.
PLAYER_TURN_SPEED = 300

# Movement speed of the player in pixels per second.
PLAYER_SPEED = 200

# Maximum number of seconds between consecutive shots.
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3

# Speed at which bullets travel after being fired.
PLAYER_SHOOT_SPEED = 500

# ---------------------------------------------------------------------------
# Asteroid Configuration
# ---------------------------------------------------------------------------

# Radius of the smallest asteroid that can exist.
ASTEROID_MIN_RADIUS = 20

# Number of asteroid size levels available.
ASTEROID_KINDS = 3

# Time interval between automatic asteroid spawns.
ASTEROID_SPAWN_RATE_SECONDS = 0.8

# Largest asteroid radius, derived from the number of size levels.
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# ---------------------------------------------------------------------------
# Projectile Configuration
# ---------------------------------------------------------------------------

# Collision radius of a player projectile.
SHOT_RADIUS = 5
