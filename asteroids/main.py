"""
main.py

Entry point for the Asteroids game.

This module is responsible for:

    • Initializing Pygame.
    • Creating the game window.
    • Initializing sprite groups.
    • Registering sprite containers.
    • Creating all game objects.
    • Running the main game loop.
    • Updating game state.
    • Detecting collisions.
    • Rendering each frame.
    • Logging game state and gameplay events.

The game loop follows a standard structure:

    1. Process user and system events.
    2. Update all game objects.
    3. Handle collision detection.
    4. Render the current frame.
    5. Limit the frame rate.
"""

import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event, log_state
from player import Player
from shot import Shot


def main() -> None:
    """
    Initialize and run the Asteroids game.

    This function creates the game window, initializes all sprite groups,
    registers sprite containers, creates the initial game objects, and
    executes the main game loop until the player exits or loses.
    """

    # Initialize all imported Pygame modules.
    pygame.init()

    # Create the main application window.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Clock used to maintain a consistent frame rate.
    clock = pygame.time.Clock()

    # Delta time (seconds elapsed since the previous frame).
    dt = 0.0

    # -----------------------------------------------------------------
    # Sprite Groups
    # -----------------------------------------------------------------

    # Objects that receive update() calls every frame.
    updatable = pygame.sprite.Group()

    # Objects that are rendered each frame.
    drawable = pygame.sprite.Group()

    # Active asteroids.
    asteroids = pygame.sprite.Group()

    # Active player projectiles.
    shots = pygame.sprite.Group()

    # -----------------------------------------------------------------
    # Sprite Registration
    # -----------------------------------------------------------------

    # Automatically add new Player objects to these groups.
    Player.containers = (
        updatable,
        drawable,
    )

    # Automatically add new Asteroid objects to these groups.
    Asteroid.containers = (
        asteroids,
        updatable,
        drawable,
    )

    # Automatically add new Shot objects to these groups.
    Shot.containers = (
        shots,
        updatable,
        drawable,
    )

    # The asteroid field only updates—it is never drawn.
    AsteroidField.containers = (updatable,)

    # -----------------------------------------------------------------
    # Game Object Creation
    # -----------------------------------------------------------------

    # Spawn the player at the center of the screen.
    player = Player(
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2,
    )

    # Create the asteroid spawning system.
    asteroid_field = AsteroidField()

    # -----------------------------------------------------------------
    # Main Game Loop
    # -----------------------------------------------------------------

    while True:
        # Record a periodic snapshot of the game state.
        log_state()

        # -------------------------------------------------------------
        # Event Processing
        # -------------------------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # -------------------------------------------------------------
        # Game Updates
        # -------------------------------------------------------------

        # Update every object registered as updatable.
        updatable.update(dt)

        # -------------------------------------------------------------
        # Collision Detection
        # -------------------------------------------------------------

        # Detect collisions between the player and asteroids.
        # End the game immediately if a collision occurs.
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # Detect collisions between projectiles and asteroids.
        # Destroy the projectile and split the asteroid.
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

        # -------------------------------------------------------------
        # Rendering
        # -------------------------------------------------------------

        # Clear the screen.
        screen.fill("black")

        # Draw every visible object.
        for obj in drawable:
            obj.draw(screen)

        # Present the completed frame.
        pygame.display.flip()

        # -------------------------------------------------------------
        # Frame Timing
        # -------------------------------------------------------------

        # Limit execution to 60 FPS and calculate the elapsed time
        # since the previous frame.
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
