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
        pass
    def print(self, *value: Any, color=None):
        if self.state or self.temporary_state:
            print(*value) if not color else termcolor.cprint(f'{str(*value)}', color)
   
    def exit(self, error_string: str, error_value: int = 2):
        termcolor.cprint(f'{str(error_string)}', "red")
        sys.exit(error_value)

        
    def unmute(self, *value, color=None):
        self.temporary_state = True
        self.print(*value, color=color)
        self.temporary_state = True
