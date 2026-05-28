"""Exceptions for the SuperInstance SDK."""


class SuperInstanceError(Exception):
    """Base exception."""
    pass


class AgentNotFoundError(SuperInstanceError):
    """Raised when an agent is not found."""
    pass


class FleetConnectionError(SuperInstanceError):
    """Raised when fleet connection fails."""
    pass


class MemoryError(SuperInstanceError):
    """Raised when memory operation fails."""
    pass
