
from .service import OwnService

class ServerService(OwnService):

    def __init__(self) -> None:
        super().__init__()

    def _create_root(self, name : str) -> dict[str, any]:
        raise NotImplementedError(f'función _create_root no implementada')

    def create_file(self, relative_path : str, name : str, body : str, rename :bool = False) -> dict[str, any]:
        raise NotImplementedError(f'función create_file no implementada')

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

