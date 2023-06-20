from .factory import CommandFactory
from .response import CommandResponse, IOType


class CommandProxy:

    def __init__(self):
        self._factory = CommandFactory()
        self.response = CommandResponse()

    def execute(self, command_name: str, args: dict[str, str]) -> bool:
        command = self._factory.get_command(command_name, args)

        # Command related validations
        if command is None:
            self.response.error(f"Comando '{command_name}' no encontrado", IOType.INPUT)
            return False

        # Parameters related validations
        if not command.validate_params():
            return False

        # Execute command
        command.info()  # ?register command execution

        command.execute()
        return command.response.overall_status


    def multiple_execution(self, file_content: str):
        pass