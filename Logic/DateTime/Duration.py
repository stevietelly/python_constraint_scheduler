class Duration:
    def __init__(self, hour: int, minute: int):
        self.hour: int = hour
        self.minute: int = minute

    def __repr__(self):
        return f"Duration(hour={self.hour}, minute={self.minute})"

    def __str__(self):
        if self.minute == 0:
            return f"{self.hour} hour(s)"
        elif self.minute == 1:
            return f"{self.hour} hour(s) and 1 minute"
        else:
            return f"{self.hour} hour(s) and {self.minute} minutes"

