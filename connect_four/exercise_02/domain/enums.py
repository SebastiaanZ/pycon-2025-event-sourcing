"""Enums for the Connect Four game.

There is probably a better way to model these enums, but it's not the
focus of this tutorial.
"""

import enum


class GameResult(enum.StrEnum):
    """The result of a game."""

    PLAYER_ONE_WON = "PLAYER_ONE_WON"
    TIED = "TIED"
    PLAYER_TWO_WON = "PLAYER_TWO_WON"


class Column(enum.StrEnum):
    """A column in a board."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


class Token(enum.Enum):
    """A token for a game of Connect Four."""

    YELLOW = "YELLOW"  # For player one
    RED = "RED"  # For player two
