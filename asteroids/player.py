"""
player.py

Defines the Player class for the Asteroids game.

The player is represented visually as a triangle and uses a circular
hitbox for collision detection. The player can:

    • Rotate left and right.
    • Move forward and backward.
    • Fire projectiles.
    • Draw itself to the screen.
    • Update its state each frame based on keyboard input.

Movement and rotation are frame rate independent through the use of
delta time (dt).
"""

import pygame

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot


class Player(CircleShape):
    """
    Represents the player's spaceship.

    The player inherits its circular collision boundary from
    CircleShape while rendering itself as a triangular spacecraft.

    Attributes
    ----------
    rotation
        Current heading of the ship in degrees.

    shot_cooldown
        Remaining time before another projectile can be fired.
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Create a player at the specified position.

        Parameters
        ----------
        x
            Initial horizontal position.

        y
            Initial vertical position.
        """

        super().__init__(x, y, PLAYER_RADIUS)

        # Current facing direction in degrees.
        self.rotation = 0

        # Time remaining before the player can shoot again.
        self.shot_cooldown = 0

    def triangle(self) -> list[pygame.Vector2]:
        """
        Compute the three vertices used to render the player's ship.

        Returns
        -------
        list[pygame.Vector2]
            Triangle vertices in screen coordinates.
        """

        # Unit vector pointing in the direction the ship is facing.
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # Unit vector perpendicular to the ship's heading.
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        # Triangle vertices.
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def draw(self, screen) -> None:
        """
        Render the player to the screen.

        Parameters
        ----------
        screen
            Pygame display surface.
        """

        pygame.draw.polygon(
            screen,
            "white",
            self.triangle(),
            LINE_WIDTH,
        )

    def rotate(self, dt: float) -> None:
        """
        Rotate the player.

        Parameters
        ----------
        dt
            Delta time in seconds. Positive values rotate clockwise,
            while negative values rotate counter-clockwise.
        """

        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        """
        Move the player along its current heading.

        Parameters
        ----------
        dt
            Delta time in seconds. Positive values move forward,
            while negative values move backward.
        """

        # Forward-facing unit vector.
        unit_vector = pygame.Vector2(0, 1)

        # Rotate the movement vector to match the ship's orientation.
        rotated_vector = unit_vector.rotate(self.rotation)

        # Scale movement using player speed and frame time.
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt

        # Update the player's world position.
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        """
        Fire a projectile if the weapon cooldown has expired.
        """

        # Prevent firing while the weapon is cooling down.
        if self.shot_cooldown > 0:
            return

        # Reset the cooldown timer.
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        # Spawn a new projectile at the player's position.
        shot = Shot(
            self.position.x,
            self.position.y,
        )

        # Launch the projectile in the direction the player is facing.
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = direction * PLAYER_SHOOT_SPEED

    def update(self, dt: float) -> None:
        """
        Update the player's state for the current frame.

        This method:

        - Updates the weapon cooldown.
        - Reads keyboard input.
        - Rotates the player.
        - Moves the player.
        - Fires projectiles.

        Parameters
        ----------
        dt
            Time elapsed since the previous frame.
        """

        # Update the remaining weapon cooldown.
        self.shot_cooldown -= dt

        # Read the current keyboard state.
        keys = pygame.key.get_pressed()

        # Rotate left.
        if keys[pygame.K_a]:
            self.rotate(-dt)

        # Rotate right.
        if keys[pygame.K_d]:
            self.rotate(dt)

        # Move forward.
        if keys[pygame.K_w]:
            self.move(dt)

        # Move backward.
        if keys[pygame.K_s]:
            self.move(-dt)

        # Fire a projectile.
        if keys[pygame.K_SPACE]:
            self.shoot()
