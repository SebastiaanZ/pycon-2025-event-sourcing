"""The `Game` aggregate root."""

from __future__ import annotations

import uuid
from typing import Self

import attrs
from connect_four_solutions.exercise_03.domain import board, enums
from connect_four_solutions.exercise_03.domain import events as events_
from connect_four_solutions.exercise_03.domain import exceptions


@attrs.define
class Game:
    """A game of Connect Four."""

    id: str = attrs.field(factory=lambda: str(uuid.uuid4()))
    player_one: str | None = None
    player_two: str | None = None
    next_player: str | None = None
    result: enums.GameResult | None = None
    historical_events: tuple[events_.GameEvent, ...] = attrs.field(factory=tuple)
    uncommitted_events: list[events_.GameEvent] = attrs.field(factory=list)
    _board: board.Board = attrs.field(init=False, factory=board.Board)

    @classmethod
    def load_from_history(
        cls, game_id: str, historical_events: list[events_.GameEvent]
    ) -> Self:
        """Restore a previous game state from a list of historic events.

        This method uses the `apply` method to apply each event to the
        state of this game instance and ensures that the events are
        stored with the game's list of events.

        Args:
            game_id: The ID of the game.
            historical_events: A list of historic events to process.
        """
        game = cls(id=game_id, historical_events=tuple(historical_events))
        for event in game.historical_events:
            game.apply(event)
        return game

    def start_game(self, player_one: str, player_two: str) -> None:
        """Start a game.

        :param player_one:
        :param player_two:
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
        if not self.has_started:
            raise exceptions.InvalidMoveError(
                "The game must be started before a move can be made."
            )
        if self.is_finished:
            raise exceptions.InvalidMoveError(
                "The game must be ongoing to make a move."
            )
        if player != self.next_player:
            raise exceptions.InvalidMoveError(
                f"It must be the turn of {player!r} for that player to" " make a move"
            )
        if not self._board.has_room_in_column(column):
            raise exceptions.InvalidMoveError(f"Column must have room for a token.")

        move_made = events_.MoveMade(player, column)
        self._process_event(move_made)
        self._check_if_game_is_finished()

    def _check_if_game_is_finished(self) -> None:
        """Check if the game is finished and emit an event if so."""
        if (result := self._board.get_result()) is None:
            return

        game_ended = events_.GameFinished(result)
        self._process_event(game_ended)

    def apply(self, event: events_.GameEvent) -> None:
        """Apply an event to the game aggregate.

        :param event: the event
        :raises ValueError: if the event is unknown
        """
        match event:
            case events_.GameStarted(player_one=player_one, player_two=player_two):
                self.player_one = player_one
                self.player_two = player_two
                self.next_player = player_one
            case events_.MoveMade(player=player, column=column):
                token = (
                    enums.Token.YELLOW if player == self.player_one else enums.Token.RED
                )
                self._board.add_move(column, token)
                self.next_player = (
                    self.player_two if player == self.player_one else self.player_one
                )
            case events_.GameFinished(result=result):
                self.result = result
                self.next_player = None
            case _:
                raise ValueError(f"Unknown event: {event!r}")

    @property
    def has_started(self) -> bool:
        """True if the game has been started.

        Since the `GameStarted` event is required to be the first event
        in the sequence of `Game`-events, we can simply check if there
        are any events for this game.
        """
        return bool(self.events)

    @property
    def events(self) -> list[events_.GameEvent]:
        """Both historical and uncommited events."""
        return list(self.historical_events) + self.uncommitted_events

    @property
    def is_finished(self) -> bool:
        """Whether the game has ended."""
        return self.result is not None

    @property
    def board(self) -> board.BoardState:
        """The current state of the board."""
        return self._board.board_state

    def _process_event(self, event: events_.GameEvent) -> None:
        """Apply the event and add it to the list of events.

        :param event: The event to process
        """
        self.apply(event)
        self.uncommitted_events.append(event)
