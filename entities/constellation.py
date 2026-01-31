from __future__ import annotations

class Constellation:
    """
    Entity for a Constellation (category of related topics).

    A constellation is a theme that organizes multiple stars (topics) into a thematic group.
    """

    # TODO: might need other information for the constellation: i.e. coordinates of the positions of stars

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
