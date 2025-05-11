import kurrentdbclient
import pytest
from kurrentdbclient import exceptions as kdb_exceptions

from connect_four import helpers


def test_equivalent_exception_for_non_existing_stream() -> None:
    """Raise the kurrentdbclient-exception for compatibility."""
    # GIVEN an instance of the InMemoryEventStoreClient
    client = helpers.InMemoryEventStoreClient()
    # AND a stream that does not exist
    stream_name = "non-existing-stream"

    # WHEN you try to get the stream
    # THEN an exception is raised
    with pytest.raises(kdb_exceptions.NotFound):
        client.get_stream(stream_name)


def test_append_single_event_to_stream() -> None:
    """The new event is stored as a RecordedEvent."""
    # GIVEN an instance of the InMemoryEventStoreClient
    client = helpers.InMemoryEventStoreClient()
    # AND the name of a stream
    stream_name = "my-stream-for-a-single-event"
    # AND an event to store
    event = kurrentdbclient.NewEvent(
        "SomethingHappened",
        data=b'{"key": "value"}\n',
    )

    # WHEN an event is appended to the stream
    client.append_to_stream(
        stream_name=stream_name,
        current_version=kurrentdbclient.StreamState.ANY,
        events=event,
    )

    # THEN the event is stored in the stream
    assert client.get_stream(stream_name) == (
        kurrentdbclient.RecordedEvent(
            type="SomethingHappened",
            data=b'{"key": "value"}\n',
            metadata=b"",
            content_type="application/json",
            id=event.id,
            stream_name=stream_name,
            stream_position=0,
            commit_position=None,
            prepare_position=None,
            recorded_at=None,
            link=None,
            retry_count=None,
        ),
    )


def test_append_multiple_events_to_stream() -> None:
    """The new events are stored as RecordedEvents."""
    # GIVEN an instance of the InMemoryEventStoreClient
    client = helpers.InMemoryEventStoreClient()
    # AND the name of a stream
    stream_name = "my-stream-for-multiple-events"
    # AND an event to store
    events = [
        kurrentdbclient.NewEvent(
            "SomethingHappened",
            data=b'{"python": "3.13"}\n',
        ),
        kurrentdbclient.NewEvent(
            "AnotherThingHappened",
            data=b'{"pycon": "2025"}\n',
        ),
    ]

    # WHEN an event is appended to the stream
    client.append_to_stream(
        stream_name=stream_name,
        current_version=kurrentdbclient.StreamState.ANY,
        events=events,
    )

    # THEN the event is stored in the stream
    assert client.get_stream(stream_name) == (
        kurrentdbclient.RecordedEvent(
            type="SomethingHappened",
            data=b'{"python": "3.13"}\n',
            metadata=b"",
            content_type="application/json",
            id=events[0].id,
            stream_name=stream_name,
            stream_position=0,
            commit_position=None,
            prepare_position=None,
            recorded_at=None,
            link=None,
            retry_count=None,
        ),
        kurrentdbclient.RecordedEvent(
            type="AnotherThingHappened",
            data=b'{"pycon": "2025"}\n',
            metadata=b"",
            content_type="application/json",
            id=events[1].id,
            stream_name=stream_name,
            stream_position=1,
            commit_position=None,
            prepare_position=None,
            recorded_at=None,
            link=None,
            retry_count=None,
        ),
    )


def test_stream_position_accounts_for_existing_events() -> None:
    """Previously committed events count towardq the stream position."""
    # GIVEN an instance of the InMemoryEventStoreClient
    client = helpers.InMemoryEventStoreClient()
    # AND the name of a stream
    stream_name = "my-stream-for-stream-position"
    # AND 20 stored event in that stream
    client.append_to_stream(
        stream_name=stream_name,
        current_version=kurrentdbclient.StreamState.ANY,
        events=[
            kurrentdbclient.NewEvent(
                "ThisHappened",
                data=b'{"key": "value"}\n',
            )
            for _ in range(20)
        ],
    )

    # WHEN a new event is appended to the stream
    client.append_to_stream(
        stream_name=stream_name,
        current_version=kurrentdbclient.StreamState.ANY,
        events=kurrentdbclient.NewEvent(
            "ThisAlsoHappened",
            data=b'{"what": "this?"}\n',
        ),
    )

    # THEN the last event has the appropriate stream position
    assert client.get_stream(stream_name)[-1].stream_position == 20
