
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from commands import CommandProxy
from auth import validate_user

app = FastAPI()


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

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
