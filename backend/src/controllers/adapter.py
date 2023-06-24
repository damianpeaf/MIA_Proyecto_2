from commands.config import CommandEnvironment
from commands.service import ServerService, OwnBucketService


def get_service_adapter(enviroment: CommandEnvironment):
    if enviroment == CommandEnvironment.SERVER:
        return ServerService()
    elif enviroment == CommandEnvironment.BUCKET:
        return OwnBucketService()
