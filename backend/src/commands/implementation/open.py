from .common_validators import is_environment, get_enviroment, is_ip, is_port, third_service_validation
from ..strategy import CommandStrategy
from ..response import CommandResponse
from ..config import FullCommandEnvironment

open_validations = [
    {
        "param_name": "type",
        "obligatory": True,
        "validator": lambda x: is_environment(x)
    },
    {
        "param_name": "ip",
        "obligatory": False,
        "validator": lambda x: is_ip(x)
    },
    {
        "param_name": "port",
        "obligatory": False,
        "validator": lambda x: is_port(x)
    },
    {
        "param_name": "name",
        "obligatory": True,
        "validator": lambda x: True
    }
]


class OpenCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response: CommandResponse):
        super().__init__("open", args,  open_validations, response)

    def execute(self):

        type_from = get_enviroment(self.args.get('type'))
        ip = self.args.get('ip')
        port = self.args.get('port')
        name = self.args.get('name')

        if not third_service_validation(self, type_from, None, ip, port):
            return

        if ip and port:
            type_from = FullCommandEnvironment.THIRD

        from_service = self.get_service_adapter(type_from, ip=ip, port=port)

        resp = from_service.get_file(name)
        self.register_execution(resp)
        self.response.data['file_content'] = resp.get('file_content')
