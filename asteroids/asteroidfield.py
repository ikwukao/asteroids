"""
Spawn and manage asteroids throughout the game.

The AsteroidField is responsible for periodically spawning asteroids
just outside the visible game area. Newly spawned asteroids are given
a random size, speed, direction, and spawn location to create varied
gameplay.
"""

import random
from collections.abc import Callable

import pygame

from asteroid import Asteroid
from constants import *

# Represents a screen edge as:
# (
#     movement_direction,
#     spawn_position_generator
# )
#
# The movement direction determines which way spawned asteroids travel,
# while the callable generates a spawn position along that edge.
Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    """Continuously spawns asteroids around the edge of the play area."""

    # Sprite groups assigned externally during game initialization.
    containers: pygame.sprite.Group

    # Definitions for each screen edge.
    #
    # Each entry contains:
    # - A normalized direction vector indicating the asteroid's initial
    #   movement direction.
    # - A callable that returns a random spawn position along that edge.
    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(
                -ASTEROID_MAX_RADIUS,
                y * SCREEN_HEIGHT,
            ),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS,
                y * SCREEN_HEIGHT,
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH,
                -ASTEROID_MAX_RADIUS,
            ),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH,
                SCREEN_HEIGHT + ASTEROID_MAX_RADIUS,
            ),
        ),
    ]

    def __init__(self) -> None:
        """Initialize the asteroid spawner."""
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Tracks elapsed time between asteroid spawns.
        self.spawn_timer = 0.0

    def spawn(
        self,
        radius: float,
        position: pygame.Vector2,
        velocity: pygame.Vector2,
    ) -> None:
        """Create a new asteroid.

        Args:
            radius: Radius of the asteroid.
            position: Initial spawn position.
            velocity: Initial movement vector.
        """
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        """Spawn new asteroids at fixed time intervals.

        Args:
            dt: Time elapsed since the previous frame, in seconds.
        """
        # Advance the spawn timer using frame-independent timing.
        self.spawn_timer += dt

        # Wait until enough time has passed before spawning another asteroid.
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # Randomly choose one of the four screen edges.
            edge = random.choice(self.edges)

            # Give the asteroid a random speed.
            speed = random.randint(40, 100)

            # Start moving toward the play area...
            velocity = edge[0] * speed

            # ...then slightly randomize the direction to make movement
            # less predictable.
            velocity = velocity.rotate(random.randint(-30, 30))

            # Generate a random spawn position along the chosen edge.
            position = edge[1](random.uniform(0, 1))

            # Choose one of the available asteroid sizes.
            kind = random.randint(1, ASTEROID_KINDS)

            # Spawn the asteroid.
            self.spawn(
                ASTEROID_MIN_RADIUS * kind,
                position,
                velocity,
            )
