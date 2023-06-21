from .common_validators import is_path, is_enviroment, get_enviroment
from ..strategy import CommandStrategy
from ..response import CommandResponse

modify_validations = [
    {
        "param_name": "path",
        "obligatory": True,
        "validator": lambda x: is_path(x)
    },
    {
        "param_name": "body",
        "obligatory": True,
        "validator": lambda x: True
    },
    {
        "param_name": "type",
        "obligatory": True,
        "validator": lambda x: is_enviroment
    }
]


class ModifyCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response : CommandResponse):
        super().__init__("modify", args,  modify_validations, response)

    def execute(self):
        
        path = self.args.get("path")
        body = self.args.get("body")
        enviroment = get_enviroment(self.args.get('type'))

        service = self.get_service_adapter(enviroment)

        resp = service.modify_file(path, body)
        self.register_execution(resp)
