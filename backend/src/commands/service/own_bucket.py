
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
            Key = ROOT_NAME,
        )

        return root
    
    def _get_path(self, relative_path : str) -> str:
        r_path = relative_path
        if relative_path[0] == '/':
            r_path = relative_path[1:]

        return path.join(ROOT_NAME, r_path)
    
    def create_file(self, relative_path : str, name : str, body : str, rename :bool = False) -> dict[str, any]:
        resp = self._default_response()

        target_path = self._get_path(relative_path)
        full_path = path.join(target_path, name)

        # validate if file exists in the bucket
        
        obj = list(self._s3_bucket.objects.filter(Prefix=full_path))

        if len(obj) > 0:
            if rename:
                new_name = self._get_unique_name(relative_path, name)
                full_path = path.join(target_path, new_name)
            else:
                self._add_error(f'El archivo {name} ya existe', resp)
                return resp
            
        # create file
        self._s3_bucket.put_object(
            Key = full_path,
            Body = body
        )

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
                Key = target_path,
                Body = body
            )
            self._add_success(f'Se modificó el archivo {relative_path}', resp)
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            self._add_error(f'Error al modificar el archivo: {error_code} - {error_message}', resp)
            
        return resp
        

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

