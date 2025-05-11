"""The `Game` aggregate root."""

from __future__ import annotations

import attrs

from connect_four.exercise_02.domain import board as cf_board
from connect_four.exercise_02.domain import enums
from connect_four.exercise_02.domain import events as events_
from connect_four.exercise_02.domain import exceptions


@attrs.define
class Game:
    """A game of Connect Four."""

    player_one: str | None = None
    player_two: str | None = None
    next_player: str | None = None
    result: enums.GameResult | None = None
    events: list[events_.GameEvent] = attrs.field(default=attrs.Factory(list))
    _board: cf_board.Board = attrs.field(
        init=True, default=attrs.Factory(cf_board.Board)
    )

    def start_game(self, player_one: str, player_two: str) -> None:
        """Start a game.

        :param player_one: the name of player one
        :param player_two: the name of player two
        """
        if self.has_started:
            raise exceptions.GameAlreadyStartedError("The game has already started.")

        game_started = events_.GameStarted(player_one, player_two)
        self._process_event(game_started)

    def make_move(self, player: str, column: enums.Column) -> None:
        """Make a move in the game.

        Args:
            player: The player that makes the move.
            column: The column the player drops a token in.
        """
        # You don't have to track the state of the board yourself. You
        # can use the instance of `Board` that you can access via the
        # attribute `self._board`.
        #
        # It has a number of handy methods:
        # - `self._board.add_move(column, token)` adds a token to the
        #   specified column.
        # - `self._board.has_room_in_column(column)` returns `True` if
        #   a column has room for a token.
        # - `self._board.get_result()` returns the result of the game
        #   in the form of an enum value. If the game is not finished,
        #   this method returns `None`.
        #
        # You will have to determine the token color of the player based
        # on the player making the move. You should use the enum value
        # `enums.TOKEN.YELLOW` for player one and `enums.TOKEN.RED` for
        # player two.
        #
        # Don't forget to call `self._process_event()` with the event(s)
        # you want to add to the game. You shouldn't manipulate the
        # state here.

    @property
    def has_started(self) -> bool:
        """True if the game has been started.

        Since the `GameStarted` event is required to be the first event
        in the sequence of `Game`-events, we simply check if there are
        any events for this game.
        """
        return bool(self.events)

    def apply(self, event: events_.GameEvent) -> None:
        """Apply an event to the game aggregate.

        :param event: the event
        :raises ValueError: if the event is unknown
        """
        match event:
            case events_.GameStarted(player_one=player_one, player_two=player_two):
                self.player_one = player_one
                self.player_two = player_two
            case _:
                raise ValueError(f"Unknown event: {event}")

    @property
    def is_finished(self) -> bool:
        """Whether the game has ended."""
        return False

    @property
    def board(self) -> cf_board.BoardState:
        """The current state of the board."""
        return self._board.board_state

    def _process_event(self, event: events_.GameEvent) -> None:
        """Apply the event and add it to the list of events.

        :param event: The event to process
        """
        self.apply(event)
        self.events.append(event)
