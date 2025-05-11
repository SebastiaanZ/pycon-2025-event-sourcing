from connect_four_solutions.exercise_01.domain import events, game


def test_game_can_be_started_with_two_players() -> None:
    """Test that we can start a game with two players.

    Note: This test will fail until you've implemented the logic that
    makes it pass.
    """
    # GIVEN the name of player one
    player_one = "Arthur, King of the Britons"
    # AND the name of player two
    player_two = "Tim the Enchanter"
    # AND instance of the game
    game_instance = game.Game()

    # WHEN I start a game with the two players
    game_instance.start_game(player_one, player_two)

    # THEN player_one has been set to the name of player one
    assert game_instance.player_one == player_one
    # AND player_two has been set to the name of player two
    assert game_instance.player_two == player_two
    # AND a GameStarted event has been added to the list of events
    # If you're using attrs or dataclasses for your GameStarted event,
    # you can replace all asserts below with:
    # assert game_instance.events == [events.GameStarted(player_one, player_two)]
    assert len(game_instance.events) == 1
    [recorded_event] = game_instance.events
    assert isinstance(recorded_event, events.GameStarted)
    assert recorded_event.player_one == player_one
    assert recorded_event.player_two == player_two
