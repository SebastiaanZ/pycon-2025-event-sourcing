from __future__ import annotations

import attrs

from connect_four.exercise_03.application import repository
from connect_four.exercise_03.domain import board as board_models
from connect_four.exercise_03.domain import enums
from connect_four.exercise_03.domain import game as game_models


@attrs.define
class ConnectFourApp:
    """A Connect Four Application.

    This application service is responsible for creating and managing
    Connect Four games. It uses a game repository to store and retrieve
    games.

    You can use this application to create a new game or interact with
    existing games. You can also get the current state of a game.

    Note that the application doesn't rely on a concrete implementation
    of a game repository. Instead, it relies on the interface of a
    repository.

    See `connect_four.exercise_03.application.repository.IGameRepository`.
    """

    _game_repository: repository.IGameRepository

    def create_game(self, player_one: str, player_two: str) -> str:
        """Create a new game and start it.

        :param player_one: the ID of the first player
        :param player_two: the ID of the second player
        :return: the ID of the game that was created
        """
        game = game_models.Game()
        game.start_game(player_one, player_two)
        self._game_repository.add(game)
        return game.id

    def make_move(self, game_id: str, player: str, column: enums.Column) -> None:
        """Make a move in the specified game.

        :param game_id: the ID of the game
        :param player: The player that wants to make the move
        :param column: The column the player drops a token in
        """
        game = self._game_repository.get(game_id)
        game.make_move(player, column)
        self._game_repository.add(game)

    def get_game(self, game_id: str) -> GameState:
        """Get the current state of a game.

        :param game_id: the ID of the game
        :return: the state of the game aggregate
        """
        game = self._game_repository.get(game_id)
        return GameState(
            player_one=game.player_one,
            player_two=game.player_two,
            next_player=game.next_player,
            is_finished=game.is_finished,
            result=game.result,
            board=game.board,
        )


@attrs.define(frozen=True)
class GameState:
    """The state of a game."""

    player_one: str | None
    player_two: str | None
    next_player: str | None
    is_finished: bool
    result: enums.GameResult | None
    board: board_models.BoardState
