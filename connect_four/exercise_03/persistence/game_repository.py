"""A game repository backed by EventStoreDB."""

from __future__ import annotations

from typing import Iterable, Protocol, Sequence

import attrs
import kurrentdbclient

from connect_four.exercise_03.domain import events as domain_events
from connect_four.exercise_03.domain import game as game_


class IEventStoreClient(Protocol):
    """Interface for an EventStore client.

    The interface of the methods defined in this class is equal to the
    interface of the KurrentDBClient. This means the implementation of
    GameRepository doesn't have to know if it's talking to a "real"
    client or an in-memory client.

    Note that the actual KurrentDBClient has more methods and the two
    methods that we're going to use also have additional kwarg-only
    parameters with default values that we've omitted for simplicity.

    By default, our CLI-client and test suite use an in-memory client,
    but you can provide command line arguments to indicate that you want
    to use a real EventStoreDB client.

    See the exercise instructions for more information.
    """

    def append_to_stream(
        self,
        /,
        stream_name: str,
        *,
        current_version: int | kurrentdbclient.StreamState,
        events: kurrentdbclient.NewEvent | Iterable[kurrentdbclient.NewEvent],
    ) -> int:
        """Append new events to a stream.

        Args:
            stream_name: The name of the stream (positional-only)
            current_version: The current version of the stream, provided
              as a keyword argument. For exercise 03, this is always
              kurrentdbclient.StreamState.ANY.
            events: The event or events to append to the stream, as a
              keyword argument. If you want to append multiple events,
              you have to provide an iterable of events (e.g., a list).

        Returns:
            The commit position of the last committed event.
        """

    def get_stream(self, stream_name: str) -> Sequence[kurrentdbclient.RecordedEvent]:
        """Get events from a stream.

        Args:
            stream_name: The name of the stream you want to read form.

        Returns:
            A sequence of events from the stream in the order they were
            committed to the stream.
        """


@attrs.define
class GameRepository:
    """A repository for persisting games in EventStoreDB.

    This GameRepository implements the IGameRepository interface, as
    expected by the ConnectFourApp application service.

    See `connect_four.exercise_03.application.repository.IGameRepository` for the
    Protocol defining the required interface.
    """

    _client: IEventStoreClient

    def add(self, game: game_.Game) -> None:
        """Add a game to the repository.

        :param game: The game to save
        :return: The ID of the game that was saved
        """
        # - First, serialize the events from the game to a list of
        #   kurrentdbclient.NewEvent objects.
        #

        # - Second, use self._client.append_to_stream to commit the
        #   events to the event stream in the event store. See the
        #   interface above for the method signature.

    def get(self, game_id: str) -> game_.Game:
        """Get a game from the repository.

        :param game_id: The ID of the game
        :return: An instance of game after applying the stored events to
            ensure the game is in the correct state
        """
        # - First, use self._client.get_stream to get the events from
        #   the event stream in the event store. See the interface
        #   above for the method signature.

        # - Second, deserialize the events to a list of domain events.

        # - Third, create a new game instance, apply the events to it,
        #   and return the instance.


def _map_domain_event_to_eventstore_event(
    event: domain_events.GameEvent,
) -> kurrentdbclient.NewEvent:
    """Map a domain event to an eventstore event.

    :param event: the domain event to map
    :return: an eventstore event that can be persisted in EventStoreDB
    """


def _map_eventstore_event_to_domain_event(
    event: kurrentdbclient.RecordedEvent,
) -> domain_events.GameEvent:
    """Map an eventstore event to a domain event.

    :param event: the eventstore event to map
    :return: the equivalent domain event
    """
