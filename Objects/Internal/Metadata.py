from Data.Validators.Structure import VALID_GENERATOR_TYPES
from Errors.Exception import InvalidGeneratorType
class InputMetadata:
    def __init__(self, input_version, generator_type, generator_version) -> None:
        self.input_version = input_version
        self.generator_version = generator_version
        self.generator_type = generator_type

        if generator_type not in VALID_GENERATOR_TYPES: raise InvalidGeneratorType(self.generator_type)

        
        