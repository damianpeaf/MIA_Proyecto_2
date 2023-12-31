from datetime import datetime
from enum import Enum, auto

class IOType(Enum):
    INPUT = auto()
    OUTPUT = auto()
    AUTH = auto()


class CommandMsgType(Enum):
    INFO = auto()
    ERROR = auto()
    WARNING = auto()
    SUCCESS = auto()


class CommandResponse:

    def __init__(self) -> None:
        self.output = []
        self.overall_status = False
        self.data = {}

    def info(self, message: str, operation_type: IOType = IOType.OUTPUT):
        self._add_msg(message, CommandMsgType.INFO, operation_type)

    def error(self, message: str, operation_type: IOType = IOType.OUTPUT):
        self._add_msg(message, CommandMsgType.ERROR, operation_type)

    def warning(self, message: str, operation_type: IOType = IOType.OUTPUT):
        self._add_msg(message, CommandMsgType.WARNING, operation_type)

    def success(self, message: str, operation_type: IOType = IOType.OUTPUT):
        self._add_msg(message, CommandMsgType.SUCCESS, operation_type)

    def _add_msg(self, message: str, msg_type: CommandMsgType, io_type: IOType):
        self.output.append({
            'msg_type': msg_type.name,
            'message': message,
            'io_type': io_type.name,
            'date': str(datetime.now())
        })


    def get_json(self) -> dict:
        return {
            'output': self.output,
            'overall_status': self.overall_status,
            'data': self.data,
        }