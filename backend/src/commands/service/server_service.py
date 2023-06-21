from os import path, getcwd, mkdir, makedirs

from .service import OwnService
from ..response import CommandMsgType


LOCAL_ROOT_PATH = path.abspath(path.join(getcwd(), 'archivos'))

class ServerService(OwnService):

    def __init__(self) -> None:
        super().__init__()
        self._create_root()

    def _create_root(self) -> dict[str, any]:
        if not path.exists(LOCAL_ROOT_PATH):
            mkdir(LOCAL_ROOT_PATH)
    
    def _get_path(self, relative_path : str) -> str:
        r_path = relative_path
        if relative_path[0] == '/':
            r_path = relative_path[1:]

        return path.join(LOCAL_ROOT_PATH, r_path)
 
    def create_file(self, relative_path : str, name : str, body : str, rename :bool = False) -> dict[str, any]:
        resp = self._default_response()

        target_path = self._get_path(relative_path)

        makedirs(target_path, exist_ok=True) # create directory if not exists

        full_path = path.join(target_path, name)

        if path.exists(full_path):
            if rename:
                new_name = self._get_unique_name(relative_path, name)
                full_path = path.join(target_path, new_name)
            else:
                self._add_error(f'El archivo {name} ya existe', resp)
                return resp
            
        with open(full_path, 'w') as f:
            f.write(body)

        self._add_success(f'Se creó el archivo {name}', resp)
        return resp


    def create_directory(self, relative_path : str, name : str, rename : bool = False) -> dict[str, any]:
        raise NotImplementedError(f'función create_directory no implementada')

    def delete_file(self, relative_path : str, name : str) -> dict[str, any]:
        raise NotImplementedError(f'función delete_file no implementada')

    def delete_all(self) -> dict[str, any]:
        raise NotImplementedError(f'función delete_all no implementada')

    def delete_directory_content(self, relative_path : str, name : str) -> dict[str, any]:
        raise NotImplementedError(f'función delete_directory_content no implementada')

    def modify_file(self, relative_path : str, body : str) -> dict[str, any]:
        raise NotImplementedError(f'función modify_file no implementada')

    def rename_resource(self, relative_path : str, new_name : str) -> dict[str, any]:
        raise NotImplementedError(f'función rename_resource no implementada')

    def _get_unique_name(self, relative_path : str, name : str) -> str:
        raise NotImplementedError(f'función _get_unique_name no implementada')

    def copy_structure(self, structure : dict[str, any], rename : bool) -> bool:
        raise NotImplementedError(f'función copy_structure no implementada')

    def get_strucutre(self, from_relative_path :str, to_relative_path : str) -> dict[str, any]:
        raise NotImplementedError(f'función get_strucutre no implementada')

    def get_file(self, from_relative_path :str, name : str) -> dict[str, any]:
        raise NotImplementedError(f'función get_file no implementada')

