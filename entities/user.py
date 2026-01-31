from __future__ import annotations
"""User entity

Contains a small User class with id, name, email and helper methods.
"""
from typing import Dict


class User:
    """Entity for a user in the system.

    Attributes:
    - `id`: unique integer identifier
    - `name`: user's name
    - `email`: user's contact email
    """
    id: str
    name: str
    email: str

    def __init__(self, id: str, name: str, email: str):
        """Create a User instance with the provided id, name, and email."""
        self.id = id
        self.name = name
        self.email = email

    def as_dict(self) -> Dict[str, object]:
        """Return a plain dict representation suitable for persistence or JSON serialization."""
        return {"id": self.id, "name": self.name, "email": self.email}

    def display_name(self) -> str:
        """Return a preferred display name for the user (currently the full name)."""
        return self.name
