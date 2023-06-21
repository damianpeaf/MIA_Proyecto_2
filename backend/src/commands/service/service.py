from abc import ABC, abstractmethod

from ..response import CommandMsgType

class ThirdService(ABC):

    def __init__(self) -> None:
        super().__init__()

       
    def _add_error(self, msg : str, resp : dict[str, any]) -> None:
        resp['ok'] = False
        resp['msgs'].append({
            'type': CommandMsgType.ERROR,
            'msg': msg
        })

    def _add_success(self, msg : str, resp : dict[str, any]) -> None:
        resp['ok'] = True
        resp['msgs'].append({
            'type': CommandMsgType.SUCCESS,
            'msg': msg
        })

    def _add_warning(self, msg : str, resp : dict[str, any]) -> None:
        resp['msgs'].append({
            'type': CommandMsgType.WARNING,
            'msg': msg
        })

    def _add_info(self, msg : str, resp : dict[str, any]) -> None:
        resp['msgs'].append({
            'type': CommandMsgType.INFO,
            'msg': msg
        })

    def _default_response(self) -> dict[str, any]:
        return {
            'ok': False,
            'msgs': []
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