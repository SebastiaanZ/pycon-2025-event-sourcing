"""Visualize a Connect Four board as a string.

This visualization contains color codes for pretty printing in a
terminal that supports it. It may look a bit funky in a terminal that
does not.
"""

import colorama
from connect_four_solutions.exercise_03.domain import enums
from connect_four_solutions.exercise_03.domain.board import BoardState


def _colorize_string(string: str, color: str) -> str:
    """Colorize a string.

    :param string: the string to colorize
    :param color: the color to use
    :return: the colorized string
    """
    return f"{color}{string}{colorama.Style.RESET_ALL}"


def _colorize_token(token: enums.Token) -> str:
    """Colorize a token based on its type.

    :param token: the token to colorize
    :return: the colorized token
    """
    color = (
        colorama.Fore.LIGHTRED_EX
        if token == enums.Token.RED
        else colorama.Fore.LIGHTYELLOW_EX
    )
    return _colorize_string("●", color)


def generate_board_string(board_state: BoardState) -> str:
    """Generate a string representation of the board.

    :param board_state: the state of the board
    :return: a string representation of the board
    """
    board = [[" " for _ in range(7)] for _ in range(6)]

    # Fill the board based on the moves
    for col, player_moves in board_state.items():
        for row, player in enumerate(player_moves):
            board[5 - row][ord(col) - ord("A")] = _colorize_token(player)

    # Define the top border with column numbers
    # Define the top border with column numbers
    top_border = _colorize_string(
        "  A   B   C   D   E   F   G", colorama.Fore.LIGHTWHITE_EX
    )
    horizontal_border = _colorize_string(
        "╔═══╦═══╦═══╦═══╦═══╦═══╦═══╗", colorama.Fore.BLUE
    )
    row_separator = _colorize_string(
        "╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣", colorama.Fore.BLUE
    )
    bottom_border = _colorize_string(
        "╚═══╩═══╩═══╩═══╩═══╩═══╩═══╝", colorama.Fore.BLUE
    )
    separator = _colorize_string("║", colorama.Fore.BLUE)

    # Generate the board string
    board_string = [top_border, horizontal_border]
    for row in board[:-1]:
        board_string.append(
            f"{separator} " + f" {separator} ".join(row) + f" {separator}"
        )
        board_string.append(row_separator)
    # Add the last row without a row separator afterward
    board_string.append(
        f"{separator} " + f" {separator} ".join(board[-1]) + f" {separator}"
    )
    board_string.append(bottom_border)

    return "\n".join(board_string)
