from .common_validators import is_environment, get_enviroment, is_ip, is_port, third_service_validation
from ..strategy import CommandStrategy
from ..response import CommandResponse
from ..config import FullCommandEnvironment

recovery_validations = [
    {
        "param_name": "type_to",
        "obligatory": True,
        "validator": lambda x: is_environment(x)
    },
    {
        "param_name": "type_from",
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


class RecoveryCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response: CommandResponse):
        super().__init__("recovery", args,  recovery_validations, response)

    def execute(self):

        type_to = get_enviroment(self.args.get('type_to'))
        type_from = get_enviroment(self.args.get('type_from'))
        ip = self.args.get('ip')
        port = self.args.get('port')
        name = self.args.get('name')

        if not third_service_validation(self, type_from, type_to, ip, port):
            return

        if ip and port:
            type_from = FullCommandEnvironment.THIRD

        to_service = self.get_service_adapter(type_to)
        from_service = self.get_service_adapter(type_from, ip=ip, port=port)

        # get structure that will be recoveryed
        from_service.on_root = True
        resp = from_service.get_structure(f'/{name}', '/')
        self.register_execution(resp)

        if not resp.get('structure'):
            return

        # transfer structure to recovery
        resp = to_service.copy_structure(resp, False)
        self.register_execution(resp)
