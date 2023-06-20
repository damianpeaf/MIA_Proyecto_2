
from fastapi import FastAPI, Request
from pydantic import BaseModel
from commands import CommandProxy
import datetime

app = FastAPI()


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
        return {"error": str(e)}
    
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
