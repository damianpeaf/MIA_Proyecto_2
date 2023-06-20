from .common_validators import is_path, is_enviroment, get_enviroment
from ..strategy import CommandStrategy
from ..response import CommandResponse

copy_validations = [
    {
        "param_name": "from",
        "obligatory": True,
        "validator": lambda x: is_path(x)
    },
    {
        "param_name": "to",
        "obligatory": True,
        "validator": lambda x: is_path(x)
    },
    {
        "param_name": "type_to",
        "obligatory": True,
        "validator": lambda x: is_enviroment(x)
    },
    {
        "param_name": "type_from",
        "obligatory": True,
        "validator": lambda x: is_enviroment(x)
    }
]


class CopyCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response : CommandResponse):
        super().__init__("copy", args,  copy_validations, response)

    def execute(self):
       
        
        from_path = self.args.get('from')
        to_path = self.args.get('to')
        type_to = get_enviroment(self.args.get('type_to'))
        type_from = get_enviroment(self.args.get('type_from'))

        from_service = self.get_service_adapter(type_from)
        to_service = self.get_service_adapter(type_to)

        resp = from_service.get_strucutre(from_path, to_path)
        self.register_execution(resp)

        if not resp.get('structure'):
            return
        
        resp = to_service.copy_structure(resp.get('structure'), False)
        self.register_execution(resp)

