"""Test suite for the exercises."""


def pytest_addoption(parser) -> None:
    """Add pytest command line option for using a KurrentDB backend."""
    parser.addoption(
        "--use-kurrentdb",
        action="store_true",
        help="Use KurrentDB while running tests",
    )
