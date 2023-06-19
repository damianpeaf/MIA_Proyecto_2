from analyzer.lexer import lexer

lexer.input('ls -l -a -h -s "hola mundo"')

while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)

print("proyecto 2 MIA")
