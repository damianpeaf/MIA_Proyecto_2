from analyzer.lexer import lexer
from fastapi import FastAPI

lexer.input('ls -l -a -h -s "hola mundo"')

while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)


app = FastAPI()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
