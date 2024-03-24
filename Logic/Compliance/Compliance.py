from typing import List



class Compliance:
    def __init__(self) -> None:
      

        self.sessions_holder: List[int] = list()
        
    
    def AddSessionIdentifiers(self, *sessionIdentifier: int):
        self.sessions_holder.extend(sessionIdentifier)
    
