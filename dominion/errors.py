"""This module defines all custom Dominion error types.

"""


class DominionError(Exception):
    """A standard type for catching various foreseen errors."""
    pass


class DominionPassError(Exception):
    """A class for catching when players pass their turn."""
    pass


class DominionQuitError(Exception):
    """A class for catching when a player quits the game."""
    pass
