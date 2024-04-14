from Objects.Internal.Preference.Preference import Rule


class Room:
    """
        This is the physical structure under which a session is set in
        params
        
    """
    def __new__(cls, *args, **kwargs):
        inst = object.__new__(cls)
        return inst

    def __init__(self, identifier: int, capacity: int, preferences: Rule):
        
      
        self.identifier: int = identifier
        self.capacity: int = capacity
        self.preferences = preferences

        
    def __str__(self):
        return f'Room:->{self.identifier}'

    def __repr__(self):
        return f'Room: {self.identifier}'

    def __eq__(self, other):
        """
        Room Equality -> if equal
        Returns Boolean
        """
        if not isinstance(other, Room): return False
        if self.identifier == other.identifier:
            return True
        return False

    def __ne__(self, other):
        """
        Room Inequality -> if not equal
        Returns Boolean
        """
        if not self == other:
            return True
        return False
    def __hash__(self) -> int:
        return hash((self.identifier, self.capacity))