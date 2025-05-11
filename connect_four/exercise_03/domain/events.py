"""For an eventful game of Connect Four."""

from __future__ import annotations

from typing import TypeAlias

import attrs

from connect_four.exercise_03.domain import enums

# Add event types that you create to this TypeAlias.
GameEvent: TypeAlias = "GameStarted | MoveMade | GameFinished"


@attrs.define(frozen=True)
class GameStarted:
    """A game has started."""

    player_one: str
    player_two: str


@attrs.define(frozen=True)
class MoveMade:
    """A move has been made."""

    player: str
    column: enums.Column


@attrs.define(frozen=True)
class GameFinished:
    """A game has finished."""

    result: enums.GameResult
