"""
Asteroid game object.

This module defines the Asteroid class, which represents moving obstacles
in the game. Asteroids travel at a constant velocity and can split into
two smaller asteroids when destroyed, creating the classic gameplay
mechanic from the Asteroids arcade game.
"""

import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    """A moving asteroid with collision and splitting behavior."""

    def __init__(self, x: float, y: float, radius: float) -> None:
        """Initialize an asteroid.

        Args:
            x: Initial x-coordinate of the asteroid.
            y: Initial y-coordinate of the asteroid.
            radius: Radius of the asteroid's collision boundary.
        """
        super().__init__(x, y, radius)

    def draw(self, screen) -> None:
        """Render the asteroid as a white outlined circle.

        Args:
            screen: The Pygame surface to draw on.
        """
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH,
        )

    def update(self, dt: float) -> None:
        """Advance the asteroid based on its current velocity.

        Movement uses delta time to remain consistent across different
        frame rates.

        Args:
            dt: Elapsed time since the previous frame, in seconds.
        """
        self.position += self.velocity * dt

    def split(self) -> None:
        """Destroy the asteroid and split it into two smaller asteroids.

        Small asteroids (those at or below the minimum radius) are simply
        removed from the game. Larger asteroids generate two smaller
        asteroids that inherit the original position but travel in
        different directions at a slightly higher speed.
        """
        # Remove the current asteroid from all sprite groups.
        self.kill()

        # Small asteroids disappear instead of splitting further.
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Record the split event for debugging and gameplay analytics.
        log_event("asteroid_split")

        # Generate a random divergence angle so the child asteroids
        # separate naturally.
        angle = random.uniform(20, 50)

        velocity1 = self.velocity.rotate(angle)
        velocity2 = self.velocity.rotate(-angle)

        # Each split reduces the asteroid's size by one level.
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(
            self.position.x,
            self.position.y,
            new_radius,
        )
        asteroid1.velocity = velocity1 * 1.2

        asteroid2 = Asteroid(
            self.position.x,
            self.position.y,
            new_radius,
        )
        asteroid2.velocity = velocity2 * 1.2
