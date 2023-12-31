from os import path, getcwd, mkdir, makedirs, remove, walk, rename
from shutil import rmtree
import time
from json import dumps

from .service import OwnService

LOCAL_ROOT_PATH = path.abspath(path.join(getcwd(), 'archivos'))


class ServerService(OwnService):

    def __init__(self) -> None:
        super().__init__()
        self._create_root()
        self.on_root = False

    def _create_root(self) -> dict[str, any]:
        if not path.exists(LOCAL_ROOT_PATH):
            mkdir(LOCAL_ROOT_PATH)

    def _get_abs_path(self, relative_path: str, aditional_resource: str = '') -> str:

        root = LOCAL_ROOT_PATH
        if self.on_root:
            root = path.abspath(getcwd())

        return path.join(root, self._get_relative_path(relative_path, aditional_resource))

    def _get_unique_name(self, relative_path: str, name: str) -> str:

        directory_path = self._get_abs_path(relative_path)

        base_name, ext = path.splitext(name)
        index = 1
        new_name = name
        while path.exists(path.join(directory_path, new_name)):
            new_name = f"{base_name}({index}){ext}"
            index += 1
        return new_name

    def create_file(self, relative_path: str, name: str, body: str, rename: bool = False) -> dict[str, any]:
        resp = self._default_response()
        target_path = self._get_abs_path(relative_path)

        makedirs(target_path, exist_ok=True)  # create directory if not exists

        full_path = path.join(target_path, name)

        if path.exists(full_path):
            if rename:
                new_name = self._get_unique_name(relative_path, name)
                full_path = path.join(target_path, new_name)
                self._add_warning(f'El archivo {name} ya existe, se renombró a {new_name}', resp)
            else:
                self._add_error(f'El archivo {name} ya existe', resp)
                return resp

        with open(full_path, 'w') as f:
            f.write(body)
            f.close()

        self._add_success(f'Se creó el archivo {name}', resp)
        return resp

    def create_directory(self, relative_path: str, name: str, rename: bool = False) -> dict[str, any]:
        resp = self._default_response()
        resp['name'] = name
        target_path = self._get_abs_path(relative_path)

        makedirs(target_path, exist_ok=True)

        full_path = path.join(target_path, name)

        if path.exists(full_path):
            if rename:
                new_name = self._get_unique_name(relative_path, name)
                full_path = path.join(target_path, new_name)
                self._add_warning(f'El directorio {name} ya existe, se renombró a {new_name}', resp)
                resp['name'] = new_name
            else:
                self._add_error(f'El directorio {name} ya existe', resp)
                return resp

        mkdir(full_path)

        self._add_success(f'Se creó el directorio {name}', resp)
        return resp

    def delete_resource(self, relative_path: str, name: str) -> dict[str, any]:
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
        self.delete_content('')

        self._add_success('Se eliminó todo el contenido', resp)
        return resp

    def delete_content(self, relative_path: str) -> dict[str, any]:
        resp = self._default_response()

        abs_path = self._get_abs_path(relative_path)

        if not path.exists(abs_path):
            self._add_error(f'El directorio {relative_path} no existe', resp)
            return resp

        # Delete file
        if path.isfile(abs_path):
            self.delete_resource(path.dirname(relative_path), path.basename(relative_path))
            return resp

        # delete content of directory
        for root, dirs, files in walk(abs_path):
            for file in files:
                remove(path.join(root, file))
            for dir in dirs:
                rmtree(path.join(root, dir))

        return resp

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

        # delete posible / at the end of relative_path
        if relative_path.endswith('/') and len(relative_path) > 1:
            relative_path = relative_path[:-1]

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

    def copy_structure(self, get_response: dict[str, any], rename: bool, exist_target=False) -> bool:
        resp = self._default_response()

        target_path = get_response['target']

        for resource in get_response['structure']:
            if resource['type'] == 'file':
                status = self.create_file(
                    target_path,
                    resource['name'],
                    resource['content'],
                    rename
                )
                print(self._get_warning_and_errors(status))
                resp['msgs'] += self._get_warning_and_errors(status)

            else:
                response = self.create_directory(target_path, resource['name'], rename)
                directory_path = path.join(target_path, response['name'])
                resp['msgs'] += self._get_warning_and_errors(response)

                if resource['content']:
                    self.copy_structure({
                        'structure': resource['content'],
                        'target': directory_path
                    }, rename)

        if self._errors_in_response(resp) > 0:
            self._add_warning('Se copió la estructura con errores', resp)
        else:
            self._add_success('Se copió la estructura', resp)
        return resp

    def get_structure(self, from_relative_path: str, to_relative_path: str) -> dict[str, any]:
        resp = self._default_response()
        resp['structure'] = []
        resp['target'] = to_relative_path

        source_path = self._get_abs_path(from_relative_path)

        if not path.exists(source_path):
            self._add_error(f'El directorio {from_relative_path} no existe', resp)
            return resp

        if path.isfile(source_path):
            self._file_data(path.dirname(source_path), path.basename(source_path), path.dirname(from_relative_path), resp)
            return resp

        for root, dirs, files in walk(source_path):

            if root != source_path:
                continue

            for _dir in dirs:

                _dir_path = self._get_relative_path(from_relative_path, _dir)
                print('Explorando directorio', _dir_path)
                _dir_content = self.get_structure(_dir_path, '').get('structure')

                resp['structure'].append({
                    'type': 'directory',
                    'name': _dir,
                    # 'path': _dir_path.replace('\\', '/'),
                    'content': _dir_content
                })

            for file in files:
                self._file_data(root, file, from_relative_path, resp)

        # self._add_success(f'Se obtuvo la estructura del directorio {from_relative_path}', resp)
        return resp

    def _file_data(self, root: str, file: str, from_relative_path: str, resp: dict[str, any]):
        file_path = self._get_relative_path(from_relative_path, file)

        with open(path.join(root, file), 'r') as f:
            file_content = f.read()

        resp['structure'].append({
            'type': 'file',
            'name': file,
            # 'path': file_path.replace('\\', '/'),
            'content': file_content
        })

    def get_file(self, from_relative_path: str) -> dict[str, any]:
        resp = self._default_response()

        source_path = self._get_abs_path(from_relative_path)

        if not path.exists(source_path) or path.isdir(source_path):
            self._add_error(f'El archivo {from_relative_path} no existe', resp)
            resp['file_content'] = None
            return resp

        with open(source_path, 'r') as f:
            resp['file_content'] = f.read()

        self._add_success(f'Se obtuvo el archivo {from_relative_path}', resp)
        return resp
