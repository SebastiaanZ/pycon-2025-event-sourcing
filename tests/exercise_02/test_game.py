import pytest

from connect_four.exercise_02.domain import events, exceptions, game


def test_game_can_be_started() -> None:
    """A game cannot be started twice."""
    # GIVEN a game
    game_obj = game.Game()
    # AND two players
    player_one = "player-1"
    player_two = "player-2"

    # WHEN the game is started
    game_obj.start_game(player_one=player_one, player_two=player_two)

    # THEN a GameStarted event has been added to the game
    assert game_obj.events == [events.GameStarted(player_one, player_two)]
    # AND the state of the game has been updated with the player names
    assert game_obj.player_one == player_one
    assert game_obj.player_two == player_two


def test_game_cannot_be_started_twice() -> None:
    """A game cannot be started twice."""
    # GIVEN a game that has already been started
    game_obj = game.Game()
    game_obj.start_game(player_one="player-1", player_two="player-2")

    # WHEN the game is started for the second time
    # THEN a GameAlreadyStartedError is raised
    with pytest.raises(exceptions.GameAlreadyStartedError):
        game_obj.start_game(player_one="player-1", player_two="player-2")


def test_player_can_make_a_move() -> None:
    """A player can make a move."""
    # GIVEN an instance of the game
    game_obj = game.Game()
    # AND that game has been started
    game_obj.start_game(player_one="player-1", player_two="player-2")

    # WHEN the first player makes a move
    game_obj.make_move(player="player-1", column=game.enums.Column.A)

    # THEN the move is registered in the game
    assert game_obj.board == {
        game.enums.Column.A: [game.enums.Token.YELLOW],
        game.enums.Column.B: [],
        game.enums.Column.C: [],
        game.enums.Column.D: [],
        game.enums.Column.E: [],
        game.enums.Column.F: [],
        game.enums.Column.G: [],
    }
    # AND the ModeMade event was added to the game_obj
    assert game_obj.events[-1] == events.MoveMade("player-1", game.enums.Column.A)
