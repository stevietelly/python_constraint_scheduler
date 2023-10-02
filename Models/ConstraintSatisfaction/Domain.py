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
    
 
    def all_variables_ascending_values(self):
        totals = [(index, len(value)) for index, value in enumerate(self.values)]
        totals.sort(key=lambda x: x[1])
        return [self.variables[total[0]] for total in totals]
    
    def all_variables_descending_values(self):
        totals = [(index, len(value)) for index, value in enumerate(self.values)]
        totals.sort(key=lambda x: x[1], reverse=True)
        return [self.variables[total[0]] for total in totals]
        
    def __str__(self) -> str:
    
        return str([f"{self.variables[i]}: {self.values[i]}" for i in range(len(self.variables))])
    
    def __repr__(self) -> str:
        return str(self)
    

        