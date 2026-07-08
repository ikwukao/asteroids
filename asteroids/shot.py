"""
shot.py

Defines the Shot class for the Asteroids game.

A Shot represents a projectile fired by the player's spaceship. Each
projectile is rendered as a small circle and travels in a straight line
at a constant velocity until it collides with an asteroid or is otherwise
removed from the game.

The Shot class inherits its position, velocity, collision radius, and
sprite behavior from the CircleShape base class.
"""

import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS


class Shot(CircleShape):
    """
    Represents a projectile fired by the player.

    A shot is a lightweight sprite with a circular collision boundary.
    Once spawned, it moves continuously in the direction it was fired
    until it is destroyed.
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Create a new projectile.

        Parameters
        ----------
        x
            Initial horizontal position.

        y
            Initial vertical position.
        """

        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen) -> None:
        """
        Render the projectile.

        Parameters
        ----------
        screen
            Pygame display surface used for rendering.
        """

        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH,
        )

    def update(self, dt: float) -> None:
        """
        Update the projectile's position.

        The projectile travels in a straight line at a constant velocity.
        Movement is scaled by the elapsed frame time to ensure frame
        rate–independent motion.

        Parameters
        ----------
        dt
            Time elapsed since the previous frame, in seconds.
        """

        # Advance the projectile according to its velocity.
        self.position += self.velocity * dt
