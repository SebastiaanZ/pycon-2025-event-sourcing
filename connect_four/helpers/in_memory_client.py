from typing import ClassVar, Iterable, Sequence

import kurrentdbclient
from kurrentdbclient import exceptions as kdb_exceptions


class InMemoryEventStoreClient:

    _store: ClassVar[dict[str, list[kurrentdbclient.RecordedEvent]]] = {}

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
        stream = self._store.setdefault(stream_name, [])
        initial_len = len(stream)
        if isinstance(events, kurrentdbclient.NewEvent):
            events = (events,)

        if not events:
            raise ValueError("No events to append")

        for i, event in enumerate(events):
            recorded_event = kurrentdbclient.RecordedEvent(
                type=event.type,
                data=event.data,
                metadata=event.metadata,
                content_type=event.content_type,
                id=event.id,
                stream_name=stream_name,
                stream_position=initial_len + i,
                commit_position=None,
                prepare_position=None,
                recorded_at=None,
                link=None,
                retry_count=None,
            )
            stream.append(recorded_event)

        return len(stream) - 1

    def get_stream(self, stream_name: str) -> Sequence[kurrentdbclient.RecordedEvent]:
        """Get events from a stream.

        Args:
            stream_name: The name of the stream you want to read form.

        Returns:
            A sequence of events from the stream in the order they were
            committed to the stream.

        Raises:
            kdb_exceptions.NotFound: If the stream does not exist.
        """
        try:
            return tuple(self._store[stream_name])
        except KeyError:
            raise kdb_exceptions.NotFound(f"Stream {stream_name!r} not found") from None
