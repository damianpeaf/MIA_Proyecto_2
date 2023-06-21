
from fastapi import FastAPI
from pydantic import BaseModel
from commands import CommandProxy
from fastapi.middleware.cors import CORSMiddleware


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
        return {"error": str(e)}
    
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
