"""
Base class for circular game objects.

This module defines the CircleShape class, the abstract foundation for all
circular entities in the game. It provides shared functionality such as:

- Position and velocity management
- Circular collision detection
- Automatic sprite group registration
- A common interface for drawing and updating

Concrete game objects (such as Player, Asteroid, and Shot) inherit from
this class and implement their own rendering and update behavior.
"""

import pygame


class CircleShape(pygame.sprite.Sprite):
    """Abstract base class for circular game objects.

    CircleShape extends ``pygame.sprite.Sprite`` so that all game entities
    can participate in Pygame's sprite group system. Subclasses inherit
    common state such as position, velocity, and collision radius while
    providing their own implementations of drawing and update logic.
    """

    # Sprite groups assigned externally during application startup.
    # Subclasses automatically join these groups when instantiated.
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        """Initialize a circular game object.

        Args:
            x: Initial x-coordinate.
            y: Initial y-coordinate.
            radius: Radius of the object's collision boundary.
        """
        # Automatically register this sprite with any configured sprite
        # groups. This allows subclasses to be managed without explicitly
        # adding each instance to every group.
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        # Position of the object's center.
        self.position: pygame.Vector2 = pygame.Vector2(x, y)

        # Current movement vector in pixels per second.
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)

        # Radius used for collision detection.
        self.radius: float = radius

    def draw(self, screen: pygame.Surface) -> None:
        """Render the object to the game window.

        Subclasses must override this method to provide their own
        rendering implementation.

        Args:
            screen: The Pygame surface to draw on.
        """
        raise NotImplementedError("Subclasses must implement draw().")

    def update(self, dt: float) -> None:
        """Update the object's state.

        Called once per frame by the game loop. Subclasses should use
        the supplied delta time to implement frame-rate independent
        movement and game logic.

        Args:
            dt: Elapsed time since the previous frame, in seconds.
        """
        raise NotImplementedError("Subclasses must implement update().")

    def collides_with(self, other: "CircleShape") -> bool:
        """Determine whether this object overlaps another circle.

        Collision detection is based on the distance between the centers
        of the two circles. Two objects are considered to collide if the
        distance between their centers is less than or equal to the sum
        of their radii.

        Args:
            other: Another CircleShape to test against.

        Returns:
            True if the objects overlap or touch; otherwise False.
        """
        distance = self.position.distance_to(other.position)
        return distance <= (self.radius + other.radius)
