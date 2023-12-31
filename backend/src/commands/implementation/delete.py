from .common_validators import is_path, is_environment, get_enviroment
from ..strategy import CommandStrategy
from ..response import CommandResponse

delete_validations = [
    {
        "param_name": "name",
        "obligatory": False,
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
        "validator": lambda x: is_environment
    }
]


class DeleteCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response : CommandResponse):
        super().__init__("delete", args,  delete_validations, response)

    def execute(self):
       
        name = '' if self.args.get('name', '') is None else self.args.get('name')
        path = self.args.get('path')
        enviroment = get_enviroment(self.args.get('type'))

        service = self.get_service_adapter(enviroment)

        resp = service.delete_resource(path, name)
        self.register_execution(resp)
