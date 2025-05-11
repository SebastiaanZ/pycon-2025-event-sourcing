from __future__ import annotations

from typing import Protocol

from connect_four.exercise_03.domain import game as game_models


class IGameRepository(Protocol):
    """Interface for a game repository.

    This interface decouples the application service from the concrete
    implementation of a repository allowing us to inject any concrete
    implementation that follows this protocol.

    One usecase is injecting a fake, in-memory repository for testing
    purposes without having to resort to patching.

    See also Hynek's video on Loose Coupling & Dependency Injection:
    - https://www.youtube.com/watch?v=uWTvMCra-_Y
    """

    def add(self, game: game_models.Game) -> None:
        """Add a game to the repository.

        :param game: The game to save
        :return: The ID of the game that was saved
        """

    def get(self, game_id: str) -> game_models.Game:
        """Get a game from the repository.

        :param game_id: The ID of the game
        :return: An instance of game after applying the stored events to
            ensure the game is in the correct state
        """
