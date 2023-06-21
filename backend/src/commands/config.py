from enum import Enum

class CommandEnvironment(Enum):
    SERVER = 1
    BUCKET = 2

class FullCommandEnvironment():
    SERVER = CommandEnvironment.SERVER
    BUCKET = CommandEnvironment.BUCKET
    THIRD = 3