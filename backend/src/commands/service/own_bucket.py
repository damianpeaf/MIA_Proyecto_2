
from dotenv import load_dotenv
from os import getenv, path
import boto3
import botocore

from .service import OwnService

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

    def _create_root(self) -> dict[str, any]:

        root = self._s3_bucket.put_object(
            Key=ROOT_NAME,
        )

        return root

    def _join(self, __path, *paths) -> str:
        return path.join(__path, *paths).replace('\\', '/')

    def _get_path(self, relative_path: str, aditional_resource: str = '') -> str:
        return self._join(ROOT_NAME, self._get_relative_path(relative_path, aditional_resource))

    def create_file(self, relative_path: str, name: str, body: str, rename: bool = False) -> dict[str, any]:
        resp = self._default_response()

        target_path = self._get_path(relative_path)
        full_path = self._join(target_path, name)

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
        print({
            'target_path': target_path,
        })

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

    def delete_directory_content(self, relative_path: str, name: str) -> dict[str, any]:
        raise NotImplementedError(
            f'función delete_directory_content no implementada')

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
        raise NotImplementedError(f'función _get_unique_name no implementada')

    def copy_structure(self, structure: dict[str, any], rename: bool) -> bool:
        raise NotImplementedError(f'función copy_structure no implementada')

    def get_structure(self, from_relative_path: str, to_relative_path: str) -> dict[str, any]:
        raise NotImplementedError(f'función get_structure no implementada')

    def get_file(self, from_relative_path: str, name: str) -> dict[str, any]:
        raise NotImplementedError(f'función get_file no implementada')
