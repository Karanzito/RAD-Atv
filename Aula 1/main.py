import json
import os

# metodo para permitir encontrar o arquivo json dentro da pasta do projeto, idependente do sistema operacional.
LOG_JSON = os.path.join('log.json') 

title = "////|Calculadora de dois numeros|////"


def json_log(a, b, opreracao, resultado): # função para salvar e abrir aquivo json
    try:

        with open(LOG_JSON, 'w') as json_f:

            log = {
                "a": a,
                "b": b,
                "operacao": opreracao,
                "resultado": resultado
            }

            json.dump(log, json_f, indent=4)

        with open(LOG_JSON, 'r') as json_f:

            row = json.load(json_f)

            log = json.dumps(row, indent=4)

            return log

    except Exception as e:

        print(f"Error: {e}")



def operacao(a, b, row_opr:str): # função para definir qual a operação, e calcular com base na operação selecionada

    opr = row_opr.strip().lower()

    if opr == 'soma':

        result = a + b

        print(f"{a} + {b} = {result}\n")

        log = json_log(a=a, b=b, opreracao=opr, resultado=result)

        print(log)

    elif opr == 'subtracao':
        
        result = a - b

        print(f"{a} - {b} = {result}\n")

        log = json_log(a=a, b=b, opreracao=opr, resultado=result)

        print(log)

    elif opr == 'multiplicacao':

        result = a * b

        print(f"{a} x {b} = {result}\n")

        log = json_log(a=a, b=b, opreracao=opr, resultado=result)

        print(log)

    elif opr == 'divisao':

        result = a // b

        print(f"{a} ÷ {b} = {result}\n")

        log = json_log(a=a, b=b, opreracao=opr, resultado=result)

        print(log)
    
    else:
        
        result == None


    return result



while True:

    print(title)

    try:

        a = int(input("Digite o primeiro número (para encerrar o programa pressione <ctrl + c>)\n> "))

        b = int(input("Digite o segundo número\n> "))

    except ValueError as e: # impede de o programa travar caso uma string ou float seja inserido

        print("Valor invalido! Digite somente numeros inteiros!\nTente novamente.\n")

        continue


    opr = input("Defina a operação ('soma', 'subtracao', 'multiplicacao', 'divisao')\n> ")

    try:
        
        resultado = operacao(a=a, b=b, row_opr=opr)

        if resultado == None:
            print("Operação invalida!\nTente novamente.\n")

            continue

    except Exception as e: # Caso algum erro não previsto aconteça, exibe uma mensagem de erro sem travar o programa

        print(f"Error: {e}")

        continue

    input("Pressione <enter> para calcular outro número. Ou pressione <ctrl + c> para encerrar.\n")