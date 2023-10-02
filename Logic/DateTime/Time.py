from Logic.DateTime.Duration import Duration


class Time:
    """
    A class to create periods in day
    """
    time_string = str

    hour = 0  # 0 to 23
    minute = 0  # 0 to 59
    state = None  # am or pm

    def __init__(self, time_string: str):
        self.time_string = time_string.lower()
        self.format()
        self.clockSystemHandling()

    def format(self):
        self.time_string = self.time_string.replace(" ", "")
        if "am" in self.time_string:
            self.state = 'am'
            self.time_string = self.time_string.replace("am", '')
        if 'pm' in self.time_string:
            self.state = 'pm'
            self.time_string = self.time_string.replace("pm", '')

        hours, minutes = self.time_string.split(":")

        self.hour, self.minute = int(hours), int(minutes)

    def clockSystemHandling(self):
        if self.state == "pm" and self.hour < 12:
            self.hour += 12

    @staticmethod
    def minuteHandling(minute: int):
        if minute < 10:
            return f'0{minute}'
        return minute

    def __repr__(self):
        return f'Time:->{self.hour}:{self.minuteHandling(self.minute)}{self.state}'

    def __str__(self):
        return f'{self.hour}:{self.minuteHandling(self.minute)}{self.state}'

    def __add__(self, other: Duration):
        """
        Time Addition
        Returns Time
        """
        if isinstance(other, type(self)) or isinstance(other, Duration):
            hour = self.hour + other.hour
            minute = self.minute + other.minute

            time = Time("0:00am")
            time.hour = hour
            time.minute = minute

            if hour > 11:
                time.state = "pm"

            return time
        elif isinstance(other, int | float):
            hour = self.hour + int(other)
            minute = int(self.minute + (other - int(other))*60)
            time = Time("0:00am")
            time.hour = hour
            time.minute = minute

            if hour > 11:
                time.state = "pm"

            return time

     

    def __sub__(self, other: Duration):
        """
        Time subtraction
        Returns Duration
        """
        hour = self.hour - other.hour
        minute = self.minute - other.minute
        duration = Duration(hour, minute)
        return duration

    def __eq__(self, other):
        """
        Time Equality -> if equal
        Returns Boolean
        """
        if self.hour == other.hour and self.minute == other.minute and other.state == self.state:
            return True
        return False

    def __ne__(self, other):
        """
        Time Inequality -> if not equal
        Returns Boolean
        """
        if not self == other:
            return True
        return False

    def __gt__(self, other):
        """
        Time Greater Than -> if time >
        Returns Boolean
        """
        if self.hour > other.hour:
            return True
        elif self.hour == other.hour and self.minute > other.minute:
            return True
        return False

    def __ge__(self, other):
        """
        Time Greater Than or Equal to -> if time >=
        Returns Boolean
        """
        if self > other or self == other:
            return True
        return False

    def __le__(self, other):
        """
        Time Less Than or Equal to -> if time <=
        Returns Boolean
        """
        if self < other or self == other:
            return True
        return False



