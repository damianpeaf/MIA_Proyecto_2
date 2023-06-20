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
        self.output_msgs = []
        self.overall_status = False

    def info(self, message: str, operation_type: IOType = IOType.OUTPUT):
        self._add_msg(message, CommandMsgType.INFO, operation_type)

    def error(self, message: str, operation_type: IOType = IOType.OUTPUT):
        self._add_msg(message, CommandMsgType.ERROR, operation_type)

    def warning(self, message: str, operation_type: IOType = IOType.OUTPUT):
        self._add_msg(message, CommandMsgType.WARNING, operation_type)

    def success(self, message: str, operation_type: IOType = IOType.OUTPUT):
        self._add_msg(message, CommandMsgType.SUCCESS, operation_type)

    def _add_msg(self, message: str, msg_type: CommandMsgType, io_type: IOType):
        self.output_msgs.log_messages.append({
            'msg_type': msg_type.name,
            'message': message,
            'io_type': io_type.name,
            'date': datetime.now(),
        })

