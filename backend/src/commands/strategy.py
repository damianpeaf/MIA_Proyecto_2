from typing import Dict, List
from abc import ABC, abstractmethod

from .validator import ParamValidator
from .response import CommandResponse, IOType

class CommandStrategy(ABC):

    """
    validations looks like this:

    [
        {
            "param_name": "param1",
            "obligatory": True,
            "validator": lambda x: x == "value1"
        }
    ]

    """

    def __init__(self, command_name: str, args: dict[str, str], validations: List[Dict[str, any]], response: CommandResponse):
        super().__init__()
        self.command_name = command_name
        self.args = args
        self.response = response
        self._validator = ParamValidator(self.command_name, validations, self.response)

     

    def validate_params(self):
        return self._validator.validate(self.args)

    def error(self, error: str, operation_type: IOType = IOType.OUTPUT):
        self.response.error(f"Comando: '{self.command_name}' - {error}", operation_type)

    def success(self, message: str = ''):
        self.response.success(f'Comando {self.command_name} - {message}', IOType.OUTPUT)
        self.response.overall_status = True

    def warning(self, message: str = '', operation_type: IOType = IOType.OUTPUT):
        self.response.warning(f"Comando '{self.command_name}' - {message}", IOType.OUTPUT)

    def info(self):
        formated_args = ', '.join([f"{key}='{value}'" for key, value in self.args.items()])
        self.response.info(f"Comando {self.command_name} - {formated_args} ", IOType.INPUT)

    @abstractmethod
    def execute(self) -> bool:
        pass
