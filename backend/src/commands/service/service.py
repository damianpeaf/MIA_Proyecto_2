from abc import ABC, abstractmethod

from ..response import CommandMsgType

class ThirdService(ABC):

    def __init__(self) -> None:
        super().__init__()

    def success(self, msg : str):
        return {
            'type': CommandMsgType.SUCCESS,
            'msg': msg
        }
    
    def error(self, msg : str):
        return {
            'type': CommandMsgType.ERROR,
            'msg': msg
        }
    
    def warning(self, msg : str):
        return {
            'type': CommandMsgType.WARNING,
            'msg': msg
        }
    
    def info(self, msg : str):
        return {
            'type': CommandMsgType.INFO,
            'msg': msg
        }

    @abstractmethod
    def copy_structure(self, structure : dict[str, any], rename : bool) -> bool:
        pass

    @abstractmethod
    def get_strucutre(self, from_relative_path :str, to_relative_path : str) -> dict[str, any]:
        pass

    @abstractmethod
    def get_file(self, from_relative_path :str, name : str) -> dict[str, any]:
        pass


class OwnService(ThirdService):

    @abstractmethod
    def _create_root(self, name : str) -> dict[str, any]:
        pass

    @abstractmethod
    def create_file(self, relative_path : str, name : str, body : str, rename :bool = False) -> dict[str, any]:
        pass


    @abstractmethod
    def create_directory(self, relative_path : str, name : str, rename : bool = False) -> dict[str, any]:
        pass

    @abstractmethod
    def delete_file(self, relative_path : str, name : str) -> dict[str, any]:
        pass

    @abstractmethod
    def delete_all(self) -> dict[str, any]:
        pass

    @abstractmethod
    def delete_directory_content(self, relative_path : str, name : str) -> dict[str, any]:
        pass

    @abstractmethod
    def modify_file(self, relative_path : str, body : str) -> dict[str, any]:
        pass

    @abstractmethod
    def rename_resource(self, relative_path : str, new_name : str) -> dict[str, any]:
        pass

    @abstractmethod
    def _get_unique_name(self, relative_path : str, name : str) -> str:
        pass