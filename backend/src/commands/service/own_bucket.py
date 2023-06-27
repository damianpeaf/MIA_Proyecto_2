
from dotenv import load_dotenv
from os import getenv, path
import boto3
import botocore

from .service import OwnService
from .s3_custom import s3list

load_dotenv()

AWS_ACCESS_KEY_ID = getenv('ENV_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('ENV_AWS_SECRET_ACCESS_KEY')
AWS_REGION = getenv('ENV_AWS_REGION')
AWS_BUCKET_NAME = getenv('ENV_AWS_BUCKET_NAME')
ROOT_NAME = 'archivos/'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

s3_resource = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

s3_bucket = s3_resource.Bucket(AWS_BUCKET_NAME)


class OwnBucketService(OwnService):

    def __init__(self) -> None:
        super().__init__()

        self._s3_client = s3_client
        self._s3_resource = s3_resource
        self._s3_bucket = s3_bucket

        self._root = self._create_root()
        self.on_root = False

    def _create_root(self) -> dict[str, any]:

        root = self._s3_bucket.put_object(
            Key=ROOT_NAME,
        )

        return root

    def _join(self, __path, *paths) -> str:
        return path.join(__path, *paths).replace('\\', '/')

    def _get_path(self, relative_path: str, aditional_resource: str = '') -> str:

        path = self._join(ROOT_NAME, self._get_relative_path(relative_path, aditional_resource))
        if self.on_root:
            path = self._get_relative_path(relative_path, aditional_resource)

        return path

    def _is_file(self, relative_path: str) -> bool:
        return len(relative_path.split('/')[-1].split('.')) > 1

    def create_file(self, relative_path: str, name: str, body: str, rename: bool = False) -> dict[str, any]:
        resp = self._default_response()

        target_path = self._get_path(relative_path)
        full_path = self._join(target_path, name)

        if not self._is_file(full_path):
            self._add_error(f'El archivo {name} no tiene extensión', resp)
            return resp

        # validate if file exists in the bucket
        obj = list(self._s3_bucket.objects.filter(Prefix=full_path))

        if len(obj) > 0:
            if rename:
                new_name = self._get_unique_name(relative_path, name)
                full_path = self._join(target_path, new_name)
            else:
                self._add_error(f'El archivo {name} ya existe', resp)
                return resp

        # create file
        self._s3_bucket.put_object(
            Key=full_path,
            Body=body
        )

        self._add_success(f'Se creó el archivo {name}', resp)
        return resp

    def create_directory(self, relative_path: str, name: str, rename: bool = False) -> dict[str, any]:
        raise NotImplementedError(f'función create_directory no implementada')

    def delete_resource(self, relative_path: str, name: str) -> dict[str, any]:
        resp = self._default_response()
        resource_path = self._get_relative_path(relative_path, name)
        target_path = self._get_path(relative_path, name)

        # validate if directory/file exists in the bucket

        obj = list(self._s3_bucket.objects.filter(Prefix=target_path))

        if len(obj) == 0:
            self._add_error(f"El recurso '{resource_path}' no existe", resp)
            return resp

        # Delete
        resource_type = 'archivo'
        if target_path[-1] == '/':
            resource_type = 'carpeta'

        try:

            if resource_type == 'archivo':
                self._s3_client.delete_object(
                    Bucket=AWS_BUCKET_NAME,
                    Key=target_path
                )
            else:
                for obj in self._s3_bucket.objects.filter(Prefix=target_path):
                    self._s3_client.delete_object(
                        Bucket=AWS_BUCKET_NAME,
                        Key=obj.key
                    )

            self._add_success(f'Se eliminó el {resource_type} {resource_path}', resp)
        except Exception as e:
            error_message = e.response['Error']['Message']
            self._add_error(f'Error al eliminar el {resource_type}: - {error_message}', resp)

        return resp

    def delete_all(self) -> dict[str, any]:
        resp = self._default_response()
        self.delete_resource('', '')
        self._add_success(f'Se eliminaron todos los recursos', resp)
        return resp

    def delete_content(self, relative_path: str, name: str = '') -> dict[str, any]:
        return self.delete_resource(relative_path, name)

    def modify_file(self, relative_path: str, body: str) -> dict[str, any]:
        resp = self._default_response()

        target_path = self._get_path(relative_path)

        # validate if file exists in the bucket

        obj = list(self._s3_bucket.objects.filter(Prefix=target_path))

        if len(obj) == 0:
            self._add_error(f'El archivo {relative_path} no existe', resp)
            return resp

        # modify file

        try:
            self._s3_bucket.put_object(
                Key=target_path,
                Body=body
            )
            self._add_success(f'Se modificó el archivo {relative_path}', resp)
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            self._add_error(
                f'Error al modificar el archivo: {error_code} - {error_message}', resp)

        return resp

    def rename_resource(self, relative_path: str, new_name: str) -> dict[str, any]:
        resp = self._default_response()

        target_path = self._get_path(relative_path)
        new_path = target_path.replace(target_path.split('/')[-1], new_name)
        is_file = len(target_path.split('/')[-1].split('.')) > 1

        # validate if file exists in the bucket

        obj = list(self._s3_bucket.objects.filter(Prefix=target_path))

        if len(obj) == 0:
            self._add_error(f'El recurso {relative_path} no existe', resp)
            return resp

        # Check if new name exists
        obj = list(self._s3_bucket.objects.filter(Prefix=new_path))

        if len(obj) > 0:
            self._add_error(f'El recurso {new_name} ya existe', resp)
            return resp

        # rename resource
        try:
            if is_file:
                self._rename_resource(new_path, target_path)
            else:
                for obj in self._s3_bucket.objects.filter(Prefix=target_path):
                    new_key = obj.key.replace(target_path, new_path)
                    self._rename_resource(new_key, obj.key)

            self._add_success(f'Se renombró el recurso {relative_path} a {new_name}', resp)
        except Exception as e:
            error_message = e.response['Error']['Message']
            self._add_error(f'Error al renombrar el recurso: - {error_message}', resp)

        return resp

    def _rename_resource(self, new_key: str, old_key: str) -> dict[str, any]:
        self._s3_client.copy_object(
            Bucket=AWS_BUCKET_NAME,
            CopySource={
                'Bucket': AWS_BUCKET_NAME,
                'Key': old_key
            },
            Key=new_key
        )
        self._s3_client.delete_object(
            Bucket=AWS_BUCKET_NAME,
            Key=old_key
        )

    def _get_unique_name(self, relative_path: str, name: str) -> str:

        target_path = self._get_path(relative_path)
        new_name = name
        i = 1

        while self._resource_exists(self._join(target_path, new_name)):

            if self._is_file(new_name):
                new_name = f'{name.split(".")[0]}({i}).{name.split(".")[1]}'
            else:
                new_name = f'{name}({i})'

            i += 1

        return new_name

    def copy_structure(self, get_response: dict[str, any], rename: bool, exist_target=False) -> bool:
        # ? Add a param for backup on root folder
        resp = self._default_response()

        # search for target path
        relative_target = get_response['target']
        target_path = self._get_path(relative_target)

        # validate if directory/file exists in the bucket

        if not self._resource_exists(target_path) and exist_target:
            self._add_error(f'El recurso {relative_target} no existe en el destino', resp)
            return resp

        # copy structure
        structure = get_response.get('structure', [])

        for root_item in structure:

            item_name = root_item['name']
            creation_path = self._join(target_path, item_name)

            if self._resource_exists(creation_path):

                item_type = 'El archivo' if root_item['type'] == 'file' else 'La carpeta'

                if rename:
                    new_name = self._get_unique_name(relative_target, item_name)
                    self._add_warning(f"{item_type} '{item_name}' ya existe en el destino, se renombró a {new_name}", resp)
                    item_name = new_name
                else:
                    self._add_error(f"{item_type} '{item_name}' ya existe en el destino", resp)
                    continue

            if root_item['type'] == 'file':
                re = self.create_file(relative_target, item_name, root_item['content'])
                print(re)
            elif root_item['type'] == 'directory':
                self.copy_structure({
                    'target': self._join(relative_target, item_name),
                    'structure': root_item['content']
                },
                    rename=False,
                    exist_target=False)

        if self._errors_in_response(resp) > 0:
            self._add_warning('No se completó toda la transferencia correctamente', resp)
        else:
            self._add_success('Se completó la transferencia correctamente', resp)

        return resp

    def get_structure(self, from_relative_path: str, to_relative_path: str) -> dict[str, any]:
        resp = self._default_response()
        resp['structure'] = []
        resp['target'] = to_relative_path

        source_path = self._get_path(from_relative_path)

        # validate if directory/file exists in the bucket

        objs = list(self._s3_bucket.objects.filter(Prefix=source_path))

        if not self._resource_exists(source_path):
            self._add_error(f"El recurso '{from_relative_path}' no existe en el origen", resp)
            return resp

        # get structure

        if self._is_file(source_path):
            resource = self._s3_client.get_object(
                Bucket=AWS_BUCKET_NAME,
                Key=source_path
            )
            resp['structure'].append({
                'type': 'file',
                'name': path.basename(source_path),
                'content': resource['Body'].read().decode('utf-8')
            })
            return resp

        for obj in s3list(self._s3_bucket, source_path, recursive=False):

            if obj.key == ROOT_NAME:
                continue

            if obj.key.endswith('/'):
                obj_name = obj.key.split('/')[-2]
                dir_path = self._join(from_relative_path, obj_name)
                content = self.get_structure(dir_path, '')
                resp['structure'].append({
                    'type': 'directory',
                    'name': obj_name,
                    'content': content['structure']
                })

            else:
                obj_name = path.basename(obj.key)
                file_obj = self._s3_client.get_object(
                    Bucket=AWS_BUCKET_NAME,
                    Key=obj.key
                )

                resp['structure'].append({
                    'type': 'file',
                    'name': obj_name,
                    'content': file_obj['Body'].read().decode('utf-8')
                })

        return resp

    def _resource_exists(self, key) -> bool:

        p_key = key

        if not self._is_file(key) and key[-1] != '/':
            p_key += '/'

        objs = list(self._s3_bucket.objects.filter(Prefix=p_key))

        return len(objs) > 0

    def get_file(self, from_relative_path: str) -> dict[str, any]:
        resp = self._default_response()

        source_path = self._get_path(from_relative_path)

        # Validate if file exists in the bucket

        if not self._resource_exists(source_path):
            self._add_error(f"El recurso '{from_relative_path}' no existe en el origen", resp)
            resp['file_content'] = None
            return resp
        
        if not self._is_file(source_path):
            self._add_error(f"El recurso '{from_relative_path}' no es un archivo", resp)
            resp['file_content'] = None
            return resp
        # Get file

        resource = self._s3_client.get_object(
            Bucket=AWS_BUCKET_NAME,
            Key=source_path
        )

        self._add_success(f"Se obtuvo el archivo '{from_relative_path}' correctamente", resp)
        resp['file_content'] = resource['Body'].read().decode('utf-8')

        return resp
