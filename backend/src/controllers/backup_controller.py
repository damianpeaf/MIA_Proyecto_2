from pydantic import BaseModel
from typing import Dict

from commands.implementation.common_validators import is_environment, get_enviroment
from commands.service.struct_conversion import convert_to_own, convert_to_standard
from .adapter import get_service_adapter


class BackupRequest(BaseModel):
    name: str
    type_: str
    structure: Dict

    class Config:
        fields = {
            'type_': 'type'
        }


empty_response = {
    'status': False
}


def backup_controller(request: BackupRequest):

    if not is_environment(request.type_):
        return empty_response

    environment = get_enviroment(request.type_)
    service = get_service_adapter(environment)
    service.on_root = True

    resp = service.copy_structure({
        'target': request.name,
        'structure': convert_to_own(request.structure)
    },
        rename=False,
        exist_target=False,
    )

    print(resp)

    return {
        'status': True
    }
