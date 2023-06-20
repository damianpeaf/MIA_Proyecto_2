from .response import CommandResponse
from .implementation import *
from .strategy import CommandStrategy


class CommandFactory:

    def __init__(self):
        pass

    def get_command(self, command_name: str, args: dict[str, str], response: CommandResponse) -> CommandStrategy | None:

        if command_name == 'create':
            return CreateCommand(args, response)
        elif command_name == 'delete':
            return DeleteCommand(args, response)
        elif command_name == 'copy':
            return CopyCommand(args, response)
        elif command_name == 'transfer':
            return TransferCommand(args, response)
        elif command_name == 'rename':
            return RenameCommand(args, response)
        elif command_name == 'modify':
            return ModifyCommand(args, response)
        elif command_name == 'backup':
            return BackupCommand(args, response)
        elif command_name == 'recovery':
            return RecoveryCommand(args, response)
        elif command_name == 'delete_all':
            return DeleteAllCommand(args, response)
        elif command_name == 'open':
            return OpenCommand(args, response)

        return None
 
