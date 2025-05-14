"""The `Game` aggregate root."""

from connect_four_solutions.exercise_01.domain import events, exceptions


class Game:
    """A game of Connect Four."""

    def __init__(self):
        self.player_one = None
        self.player_two = None
        self.events = []

    def start_game(self, player_one: str, player_two: str) -> None:
        """Start a new game between two players.

        :param player_one: The name of the first player.
        :param player_two: The name of the second player.
        """
        if self.has_started:
            raise exceptions.GameAlreadyStartedError("The game has already started.")

        event = events.GameStarted(player_one, player_two)
        self._process_event(event)

    @property
    def has_started(self) -> bool:
        """Return whether the game has started.

        :return: True if the game has started, False otherwise.
        """
        return bool(self.events)

    def _process_event(self, event: events.GameEvent) -> None:
        """Apply the event and add it to the list of events.

        :param event: The event to process
        """
        self.apply(event)
        self.events.append(event)

    def apply(self, event: events.GameEvent) -> None:
        """Apply a GameEvent to the game.

        :param event: The GameEvent to apply.
        """
        match event:
            case events.GameStarted(player_one=player_one, player_two=player_two):
                self.player_one = player_one
                self.player_two = player_two
            case _:
                raise ValueError(f"Unknown event: {event}")
