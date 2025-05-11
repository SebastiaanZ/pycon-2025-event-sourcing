"""For an eventful game of Connect Four."""

from __future__ import annotations

from typing import TypeAlias

import attrs

# Add event types that you create to this TypeAlias. Hint: Use a Union.
GameEvent: TypeAlias = "GameStarted"


@attrs.define(frozen=True)
class GameStarted:
    """A game has started."""

    player_one: str
    player_two: str
