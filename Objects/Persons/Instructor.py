from Objects.Internal.Preference.Preference import Rule


class Instructor:
    """
    Used to Reffer to an abitrary person in charge of leading
    a probbale session. Its an all inclusive term for Professors,
    teachers, Teaching Assistanst e.t.c
    """
    def __init__(self, identifier: int, preferences: Rule):
        self.identifier: int = identifier
        self.preferences = preferences
      

    def __eq__(self, other):
        """
        Instructor Equality -> if equal
        Returns Boolean
        """
        if isinstance(other, Instructor):
            return self.identifier == other.identifier
        return False

    def __ne__(self, other):
        """
        Instructor Inequality -> if not equal
        Returns Boolean
        """
        return not self.__eq__(other)

    def __str__(self):
        return f'Instructor: {self.identifier}'

    def __repr__(self):
        return str(self)
