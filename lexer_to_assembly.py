#Isabella Lucena Conceição
#ra1_4
from fileinput import filename
import sys
import dfa, executor

#TODO O vetor de tokens gerado pelo Analisador Léxico deve ser salvo em um arquivo .txt para uso nas próximas fases do projeto.

#recebe o nome do arquivo de teste
def recieve_file_name():
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <filename>.txt")
        exit(1)
    return sys.argv[1]

#processa o arquivo e retorna um vetor de linhas para irem ao parser
def process_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def results_file(filename, tokens):
    #processa o nome do arquivo para criar um novo nome para o arquivo de resultados
    pass

#responsável por reconhecer pedaços VÁLIDOS do código não fazer verificação da operação de expressão
def parseExpressao(linha:str) -> list[dfa.Token]:
    tokens = []
    index = 0
    while index < len(linha):
        # print(f"Analisando caractere: '{linha[index]}' no índice {index}")
        # index+= 1
        index = dfa.estado_inicial(linha,index, tokens) 
    
    return tokens


def main():
    filename = recieve_file_name()
    lines = process_file(filename)
    
    memoria = {}
    historico = []
    
    for numero_linha, linha in enumerate(lines, start=1):
        try:
            tokens = parseExpressao(linha)
            resultado = executor.executarExpressao(tokens, memoria, historico)
            
            token_values = [token.valor for token in tokens]
            print(f"Tokens na linha {numero_linha}: {token_values}")
            print(f"Resultado da linha {numero_linha}: {resultado}")
            print(f"Memória após linha {numero_linha}: {memoria}")
            print(f"Histórico após linha {numero_linha}: {historico}")
            
        except dfa.LexicalError as error:
            print(f"Erro léxico na linha {numero_linha}: {error}")
        except ValueError as error:
            print(f"Erro de valor na linha {numero_linha}: {error}")
            
if __name__ == "__main__":
    main()