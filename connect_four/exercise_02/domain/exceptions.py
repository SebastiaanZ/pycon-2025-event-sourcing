"""For when things don't go as planned."""


class ConnectFourError(Exception):
    """Base class for Connect Four exceptions."""


class GameAlreadyStartedError(ConnectFourError):
    """Raised when trying to start a game that has already started."""
