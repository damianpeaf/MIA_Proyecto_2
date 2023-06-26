
from .service import ThirdService
from ..config import CommandEnvironment


class ThirdBucketService(ThirdService):

    def __init__(self, ip: str, port: str, name: str, type_: CommandEnvironment) -> None:
        super().__init__()
        self.ip = ip
        self.port = port
        self.name = name
        self.type_ = type_

    def copy_structure(self, get_response: dict[str, any], rename: bool) -> bool:
        raise NotImplementedError(f'función copy_structure no implementada')

    def get_structure(self, from_relative_path: str, to_relative_path: str) -> dict[str, any]:
        raise NotImplementedError(f'función get_structure no implementada')

    def get_file(self, from_relative_path: str) -> dict[str, any]:
        raise NotImplementedError(f'función get_file no implementada')
