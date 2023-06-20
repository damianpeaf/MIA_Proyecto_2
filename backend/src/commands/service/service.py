from abc import ABC, abstractmethod


class ThirdService(ABC):

    @abstractmethod
    def copy_structure(self, structure : dict[str, any], rename : bool) -> bool:
        pass

    @abstractmethod
    def get_strucutre(self, from_path :str, to_path : str) -> dict[str, any]:
        pass

    @abstractmethod
    def get_file(self, from_path :str, name : str) -> bool:
        pass
