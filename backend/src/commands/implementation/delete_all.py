from .common_validators import is_enviroment, get_enviroment
from ..strategy import CommandStrategy
from ..response import CommandResponse

delete_all_validations = [
 
    {
        "param_name": "type",
        "obligatory": True,
        "validator": lambda x: is_enviroment
    }
]


class DeleteAllCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], response : CommandResponse):
        super().__init__("delete_all", args,  delete_all_validations, response)

    def execute(self):
        
        enviroment = get_enviroment(self.args.get('type'))

        service = self.get_service_adapter(enviroment)
        resp = service.delete_all()
        self.register_execution(resp)


       