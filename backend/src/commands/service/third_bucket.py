import requests

from .service import ThirdService
from .struct_conversion import convert_to_own, convert_to_standard
from ..config import CommandEnvironment


class ThirdBucketService(ThirdService):

    def __init__(self, ip: str, port: str, name: str, type_: CommandEnvironment) -> None:
        super().__init__()
        self.ip = ip
        self.port = port
        self.name = name
        self.type_ = type_

    def _get_type(self) -> str:

        print('sdlalkdjalsjd')
        print(self.type_)
        if self.type_ == CommandEnvironment.BUCKET:
            return 'bucket'
        elif self.type_ == CommandEnvironment.SERVER:
            return 'server'

        return None

    def _post_request(self, path: str, data: dict[str, any]) -> dict[str, any]:

        try:
            res = requests.post(
                f'http://{self.ip}:{self.port}/{path}',
                json=data
            ).json()
            print(res)
            return res
        except Exception as e:
            print(e)
            return None

    def copy_structure(self, get_response: dict[str, any], rename: bool) -> bool:
        resp = self._default_response()

        # backup endpoint
        data = self._post_request('backup', {
            'type': self._get_type(),
            'name': self.name,
            'structure': convert_to_standard(get_response['structure']),
        })

        if data is None:
            self._add_error('No se pudo conectar con el destino remoto', resp)
            return resp

        status = data.get('status')

        if status:
            self._add_success('Estructura copiada en el destino remoto', resp)
        else:
            self._add_error('No se pudo copiar la estructura en el destino remoto', resp)

        return resp

    def get_structure(self, from_relative_path: str, to_relative_path: str) -> dict[str, any]:
        resp = self._default_response()
        resp['target'] = to_relative_path

        # recovery endpoint
        data = self._post_request('recovery', {
            'name': self.name,
            'type': self._get_type(),
        })

        if data is None:
            self._add_error('No se pudo conectar con el origen remoto', resp)
            return resp

        if data.get('structure') is None:
            self._add_error('No se pudo recuperar la estructura del origen remoto', resp)
            return resp

        resp['structure'] = convert_to_own(data.get('structure'))

        self._add_success('Estructura recuperada del origen remoto', resp)
        return resp

    def get_file(self, from_relative_path: str) -> dict[str, any]:

        resp = self._default_response()

        # recovery endpoint
        data = self._post_request('open', {
            'name': self.name,
            'type': self._get_type(),
        })

        if data is None:
            self._add_error('No se pudo conectar con el origen remoto', resp)
            return resp

        if data.get('content') is None:
            self._add_error('No se pudo recuperar el archivo del origen remoto', resp)
            return resp

        self._add_success(f"Se obtuvo el archivo '{from_relative_path}' correctamente", resp)
        resp['file_content'] = data.get('content')

        return resp
