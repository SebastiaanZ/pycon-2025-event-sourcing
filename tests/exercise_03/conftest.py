import argparse

import kurrentdbclient
import pytest
from _pytest import fixtures

from connect_four import helpers
from connect_four.exercise_03.persistence import game_repository


@pytest.fixture(scope="session")
def event_store_client(
    request: fixtures.FixtureRequest,
) -> game_repository.IEventStoreClient:
    """Get an Event Store client.

    By default, this fixture will return an in-memory client. If you
    want to run your tests against a real KurrentDB instance, you can
    use the `--use-kurrentdb` command line option when running pytest:

        poetry run pytest --use-kurrentdb tests/exercise_03

    :return: an instance of esdbclient.EventStoreDBClient
    """
    if request.config.getoption("--use-kurrentdb"):
        return kurrentdbclient.KurrentDBClient("kdb://localhost:2113?tls=false")
    else:
        return helpers.InMemoryEventStoreClient()
