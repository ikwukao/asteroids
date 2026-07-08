"""
logger.py

Lightweight JSON Lines (JSONL) logger for Pygame applications.

This module provides two logging utilities used throughout the game:

    • log_state()
        Periodically captures snapshots of the current game state,
        including sprite groups and individual sprite properties.

    • log_event()
        Records significant gameplay events as they occur.

The generated log files are intended for debugging, automated testing,
gameplay analysis, and replay inspection without significantly impacting
runtime performance.

Output Files
------------
game_state.jsonl
    Periodic snapshots of the game's runtime state.

game_events.jsonl
    Event-driven log of gameplay actions and events.
"""

import inspect
import json
import math
from datetime import datetime
from typing import NotRequired, TypedDict


class SpriteInfo(TypedDict):
    """
    Serialized representation of a single sprite.

    Attributes
    ----------
    type
        Sprite class name.
    pos
        World position [x, y].
    vel
        Velocity vector [x, y].
    rad
        Collision radius.
    rot
        Rotation angle in degrees.
    """

    type: str
    pos: NotRequired[list[float]]
    vel: NotRequired[list[float]]
    rad: NotRequired[float]
    rot: NotRequired[float]


class GroupInfo(TypedDict):
    """
    Serialized representation of a pygame sprite group.

    Attributes
    ----------
    count
        Total number of sprites in the group.

    sprites
        Sample of serialized sprite information.
    """

    count: int
    sprites: list[SpriteInfo]


__all__ = ["log_state", "log_event"]


# ---------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------

# Target game frame rate.
_FPS = 60

# Maximum number of seconds to record state snapshots.
_MAX_SECONDS = 16

# Maximum number of sprites sampled from each sprite group.
# This prevents log files from becoming excessively large.
_SPRITE_SAMPLE_LIMIT = 10


# ---------------------------------------------------------------------
# Internal Runtime State
# ---------------------------------------------------------------------

# Tracks the current rendered frame.
_frame_count = 0

# Indicates whether each log file has been initialized.
# The first write overwrites any previous log; subsequent writes append.
_state_log_initialized = False
_event_log_initialized = False

# Timestamp marking the beginning of the current game session.
_start_time = datetime.now()


def log_state() -> None:
    """
    Capture and record the current game state.

    This function is designed to be called once per game loop iteration.
    Internally, it records approximately one snapshot per second until the
    configured logging duration has elapsed.

    Each snapshot contains:

    - Current timestamp
    - Elapsed runtime
    - Frame number
    - Screen dimensions
    - Sprite group summaries
    - Individual sprite information
    """

    global _frame_count, _state_log_initialized

    # Stop recording after the configured maximum duration.
    if _frame_count > _FPS * _MAX_SECONDS:
        return

    # Capture approximately one snapshot every second.
    _frame_count += 1
    if _frame_count % _FPS != 0:
        return

    now = datetime.now()

    # Inspect the caller's local scope so game objects can be
    # discovered automatically without explicit registration.
    frame = inspect.currentframe()
    if frame is None:
        return

    frame_back = frame.f_back
    if frame_back is None:
        return

    local_vars = frame_back.f_locals.copy()

    screen_size: list[int] = []
    game_state: dict[str, object] = {}
    sprite_info: SpriteInfo

    # Search the caller's local variables for pygame objects.
    for key, value in local_vars.items():

        # Record screen dimensions.
        if "pygame" in str(type(value)) and hasattr(value, "get_size"):
            screen_size = list(value.get_size())

        # Serialize pygame sprite groups.
        if hasattr(value, "__class__") and "Group" in value.__class__.__name__:

            sprites_data: list[SpriteInfo] = []

            # Record only a representative sample of sprites.
            for i, sprite in enumerate(value):
                if i >= _SPRITE_SAMPLE_LIMIT:
                    break

                sprite_info = {
                    "type": sprite.__class__.__name__
                }

                if hasattr(sprite, "position"):
                    sprite_info["pos"] = [
                        round(sprite.position.x, 2),
                        round(sprite.position.y, 2),
                    ]

                if hasattr(sprite, "velocity"):
                    sprite_info["vel"] = [
                        round(sprite.velocity.x, 2),
                        round(sprite.velocity.y, 2),
                    ]

                if hasattr(sprite, "radius"):
                    sprite_info["rad"] = sprite.radius

                if hasattr(sprite, "rotation"):
                    sprite_info["rot"] = round(sprite.rotation, 2)

                sprites_data.append(sprite_info)

            group_info: GroupInfo = {
                "count": len(value),
                "sprites": sprites_data,
            }

            game_state[key] = group_info

        # Serialize standalone sprite objects when no groups exist.
        if len(game_state) == 0 and hasattr(value, "position"):

            sprite_info = {
                "type": value.__class__.__name__
            }

            sprite_info["pos"] = [
                round(value.position.x, 2),
                round(value.position.y, 2),
            ]

            if hasattr(value, "velocity"):
                sprite_info["vel"] = [
                    round(value.velocity.x, 2),
                    round(value.velocity.y, 2),
                ]

            if hasattr(value, "radius"):
                sprite_info["rad"] = value.radius

            if hasattr(value, "rotation"):
                sprite_info["rot"] = round(value.rotation, 2)

            game_state[key] = sprite_info

    # Construct the snapshot entry.
    entry: dict[str, object] = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "screen_size": screen_size,
        **game_state,
    }

    # Overwrite the log on first write, then append future entries.
    mode = "w" if not _state_log_initialized else "a"

    with open("game_state.jsonl", mode) as f:
        f.write(json.dumps(entry) + "\n")

    _state_log_initialized = True


def log_event(event_type: str, **details: object) -> None:
    """
    Record a gameplay event.

    Parameters
    ----------
    event_type
        Descriptive name of the event.

    **details
        Additional event-specific data to include in the log.

    Each event is written as a single JSON object in JSON Lines (JSONL)
    format to ``game_events.jsonl``.
    """

    global _event_log_initialized

    now = datetime.now()

    event: dict[str, object] = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,
    }

    # Overwrite the log on first write, then append future entries.
    mode = "w" if not _event_log_initialized else "a"

    with open("game_events.jsonl", mode) as f:
        f.write(json.dumps(event) + "\n")

    _event_log_initialized = True
