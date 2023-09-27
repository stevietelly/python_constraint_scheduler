class Domain:
    """
    The Domain
    a holder for the variables and values
    """
    def __init__(self, variables: list, values) -> None:
        
        
        self.variables = variables
        self.values = [values for _ in range(len(variables))]

        self.taken_values = {}
    
    def get_value(self, variable):
        index = self.variables.index(variable)
        return self.values[index]
    
    def set_value(self, variable, value):
        index = self.variables.index(variable)
        self.values[index] = value
    
 

        
    
 
    def __str__(self) -> str:
    
        return str([f"{self.variables[i]}: {self.values[i]}" for i in range(len(self.variables))])
    
    def __repr__(self) -> str:
        return str(self)
    

        