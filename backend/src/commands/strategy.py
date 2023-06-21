from typing import Dict, List
from abc import ABC, abstractmethod

from .service import ServerService, OwnBucketService, ThirdBucketService

from .validator import ParamValidator
from .response import CommandResponse, IOType, CommandMsgType
from .config import FullCommandEnvironment
class CommandStrategy(ABC):

    """
    validations looks like this:

    [
        {
            "param_name": "param1",
            "obligatory": True,
            "validator": lambda x: x == "value1"
        }
    ]

    """

    def __init__(self, command_name: str, args: dict[str, str], validations: List[Dict[str, any]], response: CommandResponse):
        super().__init__()
        self.command_name = command_name
        self.args = args
        self.response = response
        self._validator = ParamValidator(self.command_name, validations, self.response)

     

    def validate_params(self):
        return self._validator.validate(self.args)

    def error(self, error: str, operation_type: IOType = IOType.OUTPUT):
        self.response.error(f"Comando: '{self.command_name}' - {error}", operation_type)

    def success(self, message: str = ''):
        self.response.success(f'Comando {self.command_name} - {message}', IOType.OUTPUT)
        self.response.overall_status = True

    def warning(self, message: str = '', operation_type: IOType = IOType.OUTPUT):
        self.response.warning(f"Comando '{self.command_name}' - {message}", IOType.OUTPUT)

    def info(self):
        formated_args = ', '.join([f"{key}='{value}'" for key, value in self.args.items()])
        self.response.info(f"Comando {self.command_name} - {formated_args} ", IOType.INPUT)

    def get_service_adapter(self, enviroment: FullCommandEnvironment, *args, **kwargs):

        if enviroment == FullCommandEnvironment.SERVER:
            return ServerService()
        elif enviroment == FullCommandEnvironment.BUCKET:   
            return OwnBucketService()
        elif enviroment == FullCommandEnvironment.THIRD:
            port = kwargs.get('port')
            ip = kwargs.get('ip')
            return ThirdBucketService(ip, port)

        raise Exception(f"Invalid enviroment: {enviroment}")

    def register_execution(self, response : dict[str, any]):
        
        try:
            if response is None:
                raise Exception("Invalid response, response is None")
            
            response['msgs']
        except KeyError:
            raise Exception("Invalid response, msgs key not found")

        for msg in response.get('msgs'):

            msg_type = msg.get('type')
            
            if msg_type == CommandMsgType.SUCCESS:
                self.success(msg.get('msg'))
            elif msg_type == CommandMsgType.WARNING:
                self.warning(msg.get('msg'))
            elif msg_type == CommandMsgType.ERROR:
                self.error(msg.get('msg'))
            elif msg_type == CommandMsgType.INFO:
                self.info(msg.get('msg'))
            else:
                raise Exception(f"Invalid message type: {msg_type}")
            

    def compute_overall_status(self):
        for msg in self.response.output:
            if msg['msg_type'] == CommandMsgType.ERROR.name:
                self.response.overall_status = False
                return
            
        self.response.overall_status = True

    @abstractmethod
    def execute(self) -> bool:
        pass
