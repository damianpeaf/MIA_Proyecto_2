from .response import CommandResponse
from .implementation import *
from .strategy import CommandStrategy


class CommandFactory:

    def __init__(self):
        pass

    def get_command(self, command_name: str, args: dict[str, str], response: CommandResponse) -> CommandStrategy | None:

        if command_name == 'create':
            return CreateCommand(args, response)
        
        return None
 
