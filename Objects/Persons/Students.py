from Objects.Internal.Preference.Preference import Rule


class Group:
    """
    A group of students means they belong to the same course and year
    """

    def __init__(self, identifier: int, total: int, preferences: Rule, units: list = None):
        self.identifier = identifier
        self.total = total
        self.preferences = preferences
        self.units =  units
    def __repr__(self) -> str:
        return f"Group:-> {self.identifier}"
    
    def __str__(self):
        return f'Group:->{self.identifier}'
    
    def __eq__(self, group) -> bool:
        return (self.identifier == group.identifier)

    def __ne__(self, group) -> bool:
        return (self.identifier != group.identifier)