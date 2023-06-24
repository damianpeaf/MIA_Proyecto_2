from pydantic import BaseModel

from commands.implementation.common_validators import is_environment, get_enviroment
from commands.service.struct_conversion import convert_to_own, convert_to_standard
from .adapter import get_service_adapter


class RecoveryRequest(BaseModel):
    name: str
    type_: str

    class Config:
        fields = {
            'type_': 'type'
        }


empty_response = {
    'structure': None
}


def recovery_controller(request: RecoveryRequest):

    if not is_environment(request.type_):
        return empty_response

    environment = get_enviroment(request.type_)
    service = get_service_adapter(environment)

    service.on_root = True

    resp = service.get_structure(
        from_relative_path=request.name,
        to_relative_path='/',
    )

    structure = convert_to_standard(resp.get('structure'))

    return {
        'structure': structure if structure != {} else None
    }
