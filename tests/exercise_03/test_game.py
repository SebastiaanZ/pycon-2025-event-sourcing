import pytest

from connect_four.exercise_03.domain import exceptions, game


def test_game_cannot_be_started_twice() -> None:
    """A game cannot be started twice."""
    # GIVEN a game that has already been started
    game_obj = game.Game()
    game_obj.start_game(player_one="player-1", player_two="player-2")

    # WHEN the game is started for the second time
    # THEN a GameAlreadyStartedError is raised
    with pytest.raises(exceptions.GameAlreadyStartedError):
        game_obj.start_game(player_one="player-1", player_two="player-2")
