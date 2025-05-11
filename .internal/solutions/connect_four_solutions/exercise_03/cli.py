import argparse
import warnings

with warnings.catch_warnings():
    import kurrentdbclient

from connect_four_solutions import helpers
from connect_four_solutions.exercise_03 import application, persistence, presentation
from connect_four_solutions.exercise_03.domain import enums

_CONNECTION_STRING = "kdb://localhost:2113?tls=false"


def _play(event_store_client: persistence.IEventStoreClient) -> None:
    repository = persistence.GameRepository(client=event_store_client)
    app = application.ConnectFourApp(game_repository=repository)

    print("Welcome to a new game of Connect Four!")
    match event_store_client:
        case kurrentdbclient.KurrentDBClient():
            store_type = "KurrentDB"
        case helpers.InMemoryEventStoreClient():
            store_type = "In-Memory Event Store"
        case _:
            raise RuntimeError("Unknown Event Store Client!")

    print(f"This version of the game uses {store_type} to store the game events.")
    print("========================================")
    print("Please enter the name of the players")
    player_one = input("Player 1: ")
    player_two = input("Player 2: ")
    if player_one == player_two:
        raise ValueError("Players must have different names.")
    game_id = app.create_game(player_one=player_one, player_two=player_two)

    print()
    print("========================================")
    print(f"Started a new game between {player_one} and {player_two}.")
    print(f"The game id is {game_id!r}", end="\n\n")

    game_state = app.get_game(game_id)
    while not game_state.is_finished:
        print(presentation.generate_board_string(game_state.board))
        print(f"Next player: {game_state.next_player}")
        app.make_move(
            game_id=game_id, player=game_state.next_player, column=_get_move()
        )
        game_state = app.get_game(game_id)
        print("\n\n")

    print(presentation.generate_board_string(game_state.board))

    print("That move finished the game and...")
    match game_state.result:
        case enums.GameResult.PLAYER_ONE_WON:
            print(f"{player_one} has won!")
        case enums.GameResult.PLAYER_TWO_WON:
            print(f"{player_two} has won!")
        case enums.GameResult.TIED:
            print("it's a tie!")
        case _:
            raise ValueError("The game has ended but the result is not recognized.")

    print("\n\nThank you for playing Connect Four!")


def _get_move() -> enums.Column:
    while True:
        column = input("Select column (A-G): ").strip().upper()
        try:
            return enums.Column(column)
        except ValueError:
            print("Invalid column. Please try again.")


def _get_client() -> persistence.IEventStoreClient:
    parser = argparse.ArgumentParser(
        prog="Connect Four CLI",
        description="Play Connect Four in the Terminal",
    )
    parser.add_argument(
        "--use-kurrentdb",
        action="store_true",
        help="Use KurrentDB instead of an in-memory Event Store",
    )
    args = parser.parse_args()
    if args.use_kurrentdb:
        return kurrentdbclient.KurrentDBClient(uri=_CONNECTION_STRING)
    else:
        return helpers.InMemoryEventStoreClient()


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    client = _get_client()
    _play(client)
