from __future__ import annotations

class Star:
    """
    name: The word/topic the star represents (i.e. "Multiplication)
    journal_ids: list of journal ids corresponding to this star
    constellation_id: the constellation this star belongs to
    """
    def __init__(self, id: str, name: str, journal_ids: list, constellation_id: str):
        self.id = id
        self.name = name
        self.journal_ids = journal_ids
        self.constellation_id = constellation_id
