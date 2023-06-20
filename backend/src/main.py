
from fastapi import FastAPI, Request

from commands import CommandProxy

app = FastAPI()


@app.post("/command")
async def command(request: Request):

    body = await request.json()
    command = body.get('command', '')
    proxy = CommandProxy()
    proxy.execute(command)

    return proxy.response.get_json()

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
