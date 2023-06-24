from .common_validators import is_path, is_environment, get_enviroment, is_ip, is_port
from ..strategy import CommandStrategy
from ..response import CommandResponse
from ..config import FullCommandEnvironment

backup_validations = [
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


class BackupCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response: CommandResponse):
        super().__init__("backup", args,  backup_validations, response)

    def execute(self):

        type_to = get_enviroment(self.args.get('type_to'))
        type_from = get_enviroment(self.args.get('type_from'))
        ip = self.args.get('ip')
        port = self.args.get('port')
        name = self.args.get('name')

        to_service = self.get_service_adapter(type_to)

        if ip and port and type_from == FullCommandEnvironment.SERVER:
            self.warning('Se tomara el puerto y la ip del bucket de destino para el backup en vez del servidor')

        if (not ip and port):
            self.warning("Faltó especificar la ip del servidor de destino, se tomara el especificado en 'type_from'")

        if (ip and not port):
            self.warning("Faltó especificar el puerto del servidor de destino, se tomara el especificado en 'type_from'")

        if ip and port:
            type_from = FullCommandEnvironment.THIRD

        from_service = self.get_service_adapter(type_from, ip=ip, port=port)

        # get structure that will be backuped
        resp = to_service.get_structure('/', '/')

        self.register_execution(resp)

        if not resp.get('structure'):
            return

        # ?!?! add backup folder to structure <- idk if this is right
        resp['structure'] = [
            {
                "type": "directory",
                "name": name,
                "content": resp.get('structure')
            }
        ]

        # transfer structure to backup
        resp = from_service.copy_structure(resp, False)
        self.register_execution(resp)
