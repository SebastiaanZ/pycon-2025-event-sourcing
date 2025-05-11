from typing import TypeAlias

import attrs

GameEvent: TypeAlias = "GameStarted"


@attrs.define(frozen=True)
class GameStarted:
    """Event that is fired when a game is started."""

    player_one: str
    player_two: str
