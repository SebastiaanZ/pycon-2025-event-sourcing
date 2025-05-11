from connect_four.exercise_01.domain import game as domain_game


def _play_game() -> None:
    game = domain_game.Game()

    print("Please enter the name of the players.")
    player_one = input("Player 1: ")
    player_two = input("Player 2: ")
    game.start_game(player_one, player_two)
    print()
    print(f"Started a new game between {game.player_one} and {game.player_two}.")
    print()
    print(f"Look at what happened: {game.events = }")


def main() -> None:
    print("Welcome to a game of Connect Four!")
    print("Have fun...", end="\n\n")
    _play_game()
    print("Thank you for playing Connect Four!")


if __name__ == "__main__":
    main()
