from .common_validators import is_path, is_enviroment
from ..strategy import CommandStrategy
from ..response import CommandResponse

delete_validations = [
    {
        "param_name": "name",
        "obligatory": True,
        "validator": lambda x: True
    },
    {
        "param_name": "path",
        "obligatory": True,
        "validator": lambda x: is_path(x)
    },
    {
        "param_name": "type",
        "obligatory": True,
        "validator": lambda x: is_enviroment
    }
]


class DeleteCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response : CommandResponse):
        super().__init__("delete", args,  delete_validations, response)

    def execute(self):
       self.success('')
