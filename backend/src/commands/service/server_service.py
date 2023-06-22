from os import path, getcwd, mkdir, makedirs, remove, walk, rename
from shutil import rmtree

from .service import OwnService

LOCAL_ROOT_PATH = path.abspath(path.join(getcwd(), 'archivos'))


class ServerService(OwnService):

    def __init__(self) -> None:
        super().__init__()
        self._create_root()

    def _create_root(self) -> dict[str, any]:
        if not path.exists(LOCAL_ROOT_PATH):
            mkdir(LOCAL_ROOT_PATH)
    
    def _get_abs_path(self, relative_path : str, aditional_resource : str = '') -> str:
        return path.join(LOCAL_ROOT_PATH, self._get_relative_path(relative_path, aditional_resource))
 
    def create_file(self, relative_path : str, name : str, body : str, rename :bool = False) -> dict[str, any]:
        resp = self._default_response()
        target_path = self._get_abs_path(relative_path)

        makedirs(target_path, exist_ok=True)  # create directory if not exists

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

    def create_directory(self, relative_path: str, name: str, rename: bool = False) -> dict[str, any]:
        raise NotImplementedError(f'función create_directory no implementada')

    def delete_resource(self, relative_path : str, name : str) -> dict[str, any]:
        resp = self._default_response()
        resource_path = self._get_relative_path(relative_path, name)
        target_path = self._get_abs_path(relative_path, name)

        if not path.exists(target_path):
            self._add_error(f"El recurso '{resource_path}' no existe", resp)
            return resp
        
        # delete directory
        if path.isdir(target_path):
            rmtree(target_path)
            self._add_success(f'Se eliminó el directorio {name}', resp)
            return resp
        
        # delete file
        if path.isfile(target_path):
            remove(target_path)
            self._add_success(f'Se eliminó el archivo {name}', resp)
            return resp

    def delete_all(self) -> dict[str, any]:
        resp = self._default_response()
        self.delete_directory_content('')

        self._add_success('Se eliminó todo el contenido', resp)
        return resp

    def delete_directory_content(self, relative_path : str) -> dict[str, any]:
        
        abs_path = self._get_abs_path(relative_path)

        # delete content
        for root, dirs, files in walk(abs_path):
            for file in files:
                remove(path.join(root, file))
            for dir in dirs:
                rmtree(path.join(root, dir))

    def modify_file(self, relative_path: str, body: str) -> dict[str, any]:
        resp = self._default_response()

        target_path = self._get_abs_path(relative_path)

        if not path.exists(target_path):
            self._add_error(f'El archivo {relative_path} no existe', resp)
            return resp

        with open(target_path, 'w') as f:
            f.write(body)

        self._add_success(f'Se modificó el archivo {relative_path}', resp)

        return resp

    def rename_resource(self, relative_path: str, new_name: str) -> dict[str, any]:
        resp = self._default_response()

        target_path = self._get_abs_path(relative_path)

        if not path.exists(target_path):
            self._add_error(f'La ruta {relative_path} no existe', resp)
            return resp

        base_path = path.dirname(target_path)

        new_path = path.join(base_path, new_name)

        if path.exists(new_path):
            self._add_error(
                f'Ya existe un recurso con el nombre {new_name}', resp
            )
            return resp

        rename(target_path, new_path)

        self._add_success(
            f'Se renombró el recurso {relative_path} a {new_name}', resp
        )

        return resp

    def _get_unique_name(self, relative_path: str, name: str) -> str:
        raise NotImplementedError(f'función _get_unique_name no implementada')

    def copy_structure(self, structure: dict[str, any], rename: bool) -> bool:
        raise NotImplementedError(f'función copy_structure no implementada')

    def get_strucutre(self, from_relative_path: str, to_relative_path: str) -> dict[str, any]:
        raise NotImplementedError(f'función get_strucutre no implementada')

    def get_file(self, from_relative_path: str, name: str) -> dict[str, any]:
        raise NotImplementedError(f'función get_file no implementada')
