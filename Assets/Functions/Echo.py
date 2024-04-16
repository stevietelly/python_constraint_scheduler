from typing import Any
import sys
import termcolor


class Echo:
    state: bool = False
    def __init__(self) -> None:
        """
        A class to approve printing specific values to the screen
        """
        self.temporary_state = False
    def print(self, *value: Any, color=None, end="\n"):
        if self.state or self.temporary_state:
            print(*value, end=end) if not color else termcolor.cprint(f'{str(*value)}', color, end=end)
   
    def exit(self, *error_string: str, error_value: int = 2):
        self.unmute(error_string[0], color="red")
        sys.exit(error_value)

        
    def unmute(self, *value, color=None, end="\n"):
        self.temporary_state = True
        self.print(*value, color=color, end=end)
        self.temporary_state = True
