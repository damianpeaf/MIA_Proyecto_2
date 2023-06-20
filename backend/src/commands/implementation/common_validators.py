from os import path

from ..config import CommandEnvironment


envs_names = [env.name.lower() for env in CommandEnvironment.__members__.values()]

def is_enviroment(value: str):

    if value is None:
        return False

    if value.lower() in envs_names:
        return True
    else:
        return False


def is_bool(value: str):

    if value is None:
        return False

    if value.lower() in ['true', 'false']:
        return True
    else:
        return False


def path_exists(value: str) -> bool:
    return True if path.exists(value) else False


def file_exists(value: str) -> bool:
    return True if path.isfile(value) else False


def is_path(value: str):

    if path.isabs(path.normpath(value)):
        return True
    else:
        return False


def get_boolean(value: str):
    if value.lower() == 'true':
        return True
    else:
        return False


def get_enviroment(value: str):
    
    if value.lower() == CommandEnvironment.BUCKET.name.lower():
        return CommandEnvironment.BUCKET
    elif value.lower() == CommandEnvironment.SERVER.name.lower():
        return CommandEnvironment.SERVER
    
    return None
