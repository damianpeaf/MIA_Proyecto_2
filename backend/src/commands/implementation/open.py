from .common_validators import is_enviroment, get_enviroment, is_ip, is_port
from ..strategy import CommandStrategy
from ..response import CommandResponse
from ..config import FullCommandEnvironment

open_validations = [
    {
        "param_name": "type",
        "obligatory": True,
        "validator": lambda x: is_enviroment(x)
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

    def __init__(self, args: dict[str, str], response : CommandResponse):
        super().__init__("open", args,  open_validations, response)

    def execute(self):
        
        type_from = get_enviroment(self.args.get('type'))
        ip = self.args.get('ip')
        port = self.args.get('port')
        name = self.args.get('name')


        if ip and port and type_from == FullCommandEnvironment.SERVER:
            self.warning('Se tomara el puerto y la ip del bucket de destino para el open en vez del servidor')

        if (not ip and port):
            self.warning("Faltó especificar la ip del servidor de destino, se tomara el especificado en 'type_from'")

        if (ip and not port):
            self.warning("Faltó especificar el puerto del servidor de destino, se tomara el especificado en 'type_from'")

        if ip and port:
            type_from = FullCommandEnvironment.THIRD

        from_service = self.get_service_adapter(type_from, ip=ip, port=port)

        resp = from_service.get_file(name)
        self.register_execution(resp)
        self.response.data['file_content'] = resp.get('file_content')