from json import dumps

from .common_validators import is_path, is_environment, get_enviroment
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
        "validator": lambda x: is_environment(x)
    },
    {
        "param_name": "type_from",
        "obligatory": True,
        "validator": lambda x: is_environment(x)
    }
]


class CopyCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response: CommandResponse):
        super().__init__("copy", args,  copy_validations, response)

    def execute(self):

        from_path = self.args.get('from')
        to_path = self.args.get('to')
        type_to = get_enviroment(self.args.get('type_to'))
        type_from = get_enviroment(self.args.get('type_from'))

        from_service = self.get_service_adapter(type_from)
        to_service = self.get_service_adapter(type_to)

        resp = from_service.get_structure(from_path, to_path)
        self.register_execution(resp)

        if not resp.get('structure'):
            return

        # print formated structure
        print(dumps(resp.get('structure'), indent=4))

        resp = to_service.copy_structure(resp, False)

        self.register_execution(resp)
