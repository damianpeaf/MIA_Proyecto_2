from pydantic import BaseModel

from commands.implementation.common_validators import is_environment, get_enviroment
from .adapter import get_service_adapter


class OpenRequest(BaseModel):
    name: str
    type_: str

    class Config:
        fields = {
            'type_': 'type'
        }


empty_response = {
    'content': None
}


def open_controller(request: OpenRequest):

    if not is_environment(request.type_):
        return empty_response

    environment = get_enviroment(request.type_)
    service = get_service_adapter(environment)

    resp = service.get_file(request.name)

    return {
        'content': resp.get('file_content')
    }
