from abc import ABC, abstractmethod
from os import path

from ..response import CommandMsgType


class ThirdService(ABC):

    def __init__(self) -> None:
        super().__init__()

    def _add_error(self, msg: str, resp: dict[str, any]) -> None:
        resp['ok'] = False
        resp['msgs'].append({
            'type': CommandMsgType.ERROR,
            'msg': msg
        })

    def _add_success(self, msg: str, resp: dict[str, any]) -> None:
        resp['ok'] = True
        resp['msgs'].append({
            'type': CommandMsgType.SUCCESS,
            'msg': msg
        })

    def _add_warning(self, msg: str, resp: dict[str, any]) -> None:
        resp['msgs'].append({
            'type': CommandMsgType.WARNING,
            'msg': msg
        })

    def _add_info(self, msg: str, resp: dict[str, any]) -> None:
        resp['msgs'].append({
            'type': CommandMsgType.INFO,
            'msg': msg
        })

    def _default_response(self) -> dict[str, any]:
        return {
            'ok': False,
            'msgs': []
        }

    def _errors_in_response(self, resp: dict[str, any]) -> int:
        return len([msg for msg in resp['msgs'] if msg['type'] == CommandMsgType.ERROR])

    def _success_in_response(self, resp: dict[str, any]) -> int:
        return len([msg for msg in resp['msgs'] if msg['type'] == CommandMsgType.SUCCESS])

    @abstractmethod
    def copy_structure(self, get_response: dict[str, any], rename: bool) -> bool:
        pass

    @abstractmethod
    def get_structure(self, from_relative_path: str, to_relative_path: str) -> dict[str, any]:
        pass

    @abstractmethod
    def get_file(self, from_relative_path: str, name: str) -> dict[str, any]:
        pass


class OwnService(ThirdService):

    def _get_relative_path(self, relative_path: str, aditional_resource: str = '') -> str:
        r_path = relative_path
        if len(relative_path.strip()) > 0 and relative_path[0] == '/':
            r_path = relative_path[1:]

        a_resource = aditional_resource
        if len(aditional_resource.strip()) > 0 and aditional_resource[0] == '/':
            a_resource = aditional_resource[1:]

        if len(a_resource.strip()) > 0:
            r_path = path.join(r_path, a_resource)

        return r_path

    @abstractmethod
    def _create_root(self, name: str) -> dict[str, any]:
        pass

    @abstractmethod
    def create_file(self, relative_path: str, name: str, body: str, rename: bool = False) -> dict[str, any]:
        pass

    @abstractmethod
    def create_directory(self, relative_path: str, name: str, rename: bool = False) -> dict[str, any]:
        pass

    @abstractmethod
    def delete_resource(self, relative_path: str, name: str) -> dict[str, any]:
        pass

    @abstractmethod
    def delete_all(self) -> dict[str, any]:
        pass

    @abstractmethod
    def delete_content(self, relative_path: str, name: str) -> dict[str, any]:
        pass

    @abstractmethod
    def modify_file(self, relative_path: str, body: str) -> dict[str, any]:
        pass

    @abstractmethod
    def rename_resource(self, relative_path: str, new_name: str) -> dict[str, any]:
        pass

    @abstractmethod
    def _get_unique_name(self, relative_path: str, name: str) -> str:
        pass
