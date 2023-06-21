from analyzer.parser import parser, ParseError

from .factory import CommandFactory
from .response import CommandResponse, IOType


class CommandProxy:

    def __init__(self):
        self._factory = CommandFactory()
        self.response = CommandResponse()

    def execute(self, command_line, line = None) -> bool:

        try:
            parsed_command = parser.parse(command_line)
        except ParseError as e:
            self.response.error(f"Error al parsear el comando '{command_line}'  {f'linea :{str(line)}' if line is not None else ''}", IOType.INPUT)
            return

        if parsed_command is None:
            self.response.error(f"Error al parsear el comando '{command_line}' linea : {str(line) if line is not None else ''}", IOType.INPUT)
            return

        command_name, args = parsed_command
        command = self._factory.get_command(command_name, args, self.response)


        # Command related validations
        if command is None:
            self.response.error(f"Comando '{command_name}' no encontrado", IOType.INPUT)
            return False

        # Parameters related validations
        if not command.validate_params():
            return False

        # Execute command
        command.info()  # ? register command execution

        command.execute()
        command.compute_overall_status()
        return command.response.overall_status


    def multiple_execution(self, file_content: str):

        line_count = 0
        for line in file_content.split('\n'):

            line_count += 1
            if line.strip() == '':
                continue

            self.execute(line, line_count)

          


