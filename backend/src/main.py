
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

from commands import CommandProxy
from auth import validate_user
from controllers import open_controller, OpenRequest, backup_controller, BackupRequest, recovery_controller, RecoveryRequest


app = FastAPI(
    title="Grupo 6 API",
    description="API para el proyecto 2 del curso manejo e implementación de archivos",
    version="1.0.0",
)

# Cors, allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class CommandRequest(BaseModel):
    command: str


@app.post("/command")
async def command(request: CommandRequest):

    try:
        command_line = request.command
        proxy = CommandProxy()
        proxy.execute(command_line)
        return proxy.response.get_json()
    except NotImplementedError as e:
        # change response status code to 501
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(e))


class AuthRequest(BaseModel):
    username: str
    password: str


@app.post("/auth")
async def auth(request: AuthRequest):

    usernsame = request.username
    password = request.password

    result = validate_user(usernsame, password)

    result.get('response').overall_status = result.get('ok', False)
    response = result.get('response').get_json()
    if result.get('ok'):
        return response

    # change response status code to 401
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)


@app.post('/open')
async def open(request: OpenRequest):
    try:
        return open_controller(request)
    except Exception as e:
        return {
            'content': None
        }


@app.post("/backup")
async def backup(request: BackupRequest):
    try:
        return backup_controller(request)
    except Exception as e:
        print(e)
        return {
            "status": False
        }


@app.post("/recovery")
async def recovery(request: RecoveryRequest):
    try:
        return recovery_controller(request)
    except Exception as e:
        print(e)
        return {
            "structure": None
        }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
