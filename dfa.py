#maquina de estados finitos ISABELLA LUCENA BCC 2026
# Implementação do Analisador léxico usando Autômatos Finitos Determinísticos (AFDs), com cada estado como uma função.
from dataclasses import dataclass

@dataclass
class Token: 
    tipo: str
    valor: str
    # memoria: int = 0

class LexicalError(Exception):
    pass

ESPACOS = {" ", "\t"}
OPERADORES_SIMPLES = {"+", "*", "%", "^"}
SUBTRACTION_OPERATOR = {"-"}
PARENTESES = {"(", ")"}
NUMEROS = set("0123456789")
LETRAS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def is_number(caractere: str) -> bool:
    return caractere in NUMEROS

def is_uppercase_letter(caractere: str) -> bool:
    return caractere in LETRAS

def retorna_token(tokens: list[Token], lexema: str, tipo: str):
    tokens.append(Token(tipo=tipo, valor=lexema))
    
def is_espaco(caractere: str) -> bool:
    return caractere in ESPACOS

def pode_iniciar_lexema(caractere: str) -> bool:
    return (
        caractere in PARENTESES
        or caractere in OPERADORES_SIMPLES
        or caractere == "-"
        or caractere == "/"
        or is_number(caractere)
        or is_uppercase_letter(caractere)
    )

def pode_terminar_token(linha: str, index: int) -> bool:
    if index >= len(linha):
        return True
    
    caractere = linha[index]
    return is_espaco(caractere) or pode_iniciar_lexema(caractere)
    
def estado_inicial(linha, index, tokens) -> int:
    """
    Estado inicial é responsável analisar o caractere atual e decidir qual estado seguir com base no tipo do caractere (número, letra, operador, etc.).
    """
    caractere = linha[index]
    
    if caractere in ESPACOS:
        return index + 1  # Ignora espaços e avança para o próximo caractere 
    
    if is_number(caractere):
        return estado_numero(linha, index, tokens)
    
    if caractere == "-":
        return estado_intermediario(linha, index, tokens)
    
    if caractere == "/":
        return estado_barra(linha, index, tokens)
    
    if caractere in OPERADORES_SIMPLES:
        return estado_operador(linha, index, tokens)
    
    if is_uppercase_letter(caractere):
        return estado_palavra(linha, index, tokens)
    
    if caractere in PARENTESES:
        return estado_parenteses(linha, index, tokens)
    
    return estado_falha(linha, index, tokens, f"Caractere inválido: '{caractere}' no índice {index}")

def estado_intermediario(linha, index, tokens) -> int:
    """
    Estado intermediário para lidar com o operador de subtração '-' que pode ser um operador ou parte de um número negativo.
    """
    proximo = index + 1 # imita o fluxo da "setinha" para ativar o próximo estado
    
    if proximo < len(linha) and is_number(linha[proximo]): 
        return estado_numero(linha, index, tokens)  # Trata como número negativo
    
    return estado_operador(linha, index, tokens)  # Trata como operador de subtração
      
def estado_parenteses(linha, index, tokens) -> int:
    """
    Estado responsável por reconhecer parênteses sem validar o balance.
    """
    
    caractere = linha[index]
    
    if caractere == "(" or caractere == ")":
        retorna_token(tokens, caractere, "PARENTHESIS")
        return index + 1
    
    return estado_falha(linha, index, tokens, f"Caractere inválido: '{caractere}' no índice {index}")
    
def estado_barra(linha, index, tokens) -> int:
    proximo = index + 1 #jeito de verificar qual o valor da próxima "setinha"
    
    if proximo < len(linha) and linha[proximo] == "/":
        return estado_barra_dupla(linha, index, tokens)
    
    if not pode_terminar_token(linha, proximo):
        return estado_falha(linha, index, tokens, "Operador '/' deve ser seguido por um delimitador válido.")
    
    retorna_token(tokens, "/", "DIVISION_OPERATOR")
    return proximo

def estado_barra_dupla(linha, index, tokens) -> int:
    segundo = index + 1
    
    if segundo >= len(linha) or linha[segundo] != "/":
        return estado_falha(linha, index, tokens, "Operador '//' malformado.")
    
    proximo = segundo + 1
    
    if not pode_terminar_token(linha, proximo):
        return estado_falha(linha, index, tokens, "Operador '//' deve ser seguido por um delimitador válido.")
    
    retorna_token(tokens, "//", "INTEGER_DIVISION_OPERATOR")
    return proximo
    
def estado_operador(linha, index, tokens) -> int:
    caractere = linha[index]
    #diferencia operadores de um caractere
    
    mapa_operadores = {
        "+": "ADDITION_OPERATOR",
        "-": "SUBTRACTION_OPERATOR",
        "*": "MULTIPLICATION_OPERATOR",
        "%": "MODULO_OPERATOR",
        "^": "EXPONENTIATION_OPERATOR"
    }
    
    if caractere not in mapa_operadores:
        return estado_falha(linha, index, tokens, f"Caractere '{caractere}' não é um operador válido.")
    
    proximo = index + 1
    
    if not pode_terminar_token(linha, proximo):
        return estado_falha(linha, index, tokens, f"Operador '{caractere}' deve ser seguido por um delimitador válido.")
    
    retorna_token(tokens, caractere, mapa_operadores[caractere])
    return proximo

def estado_palavra(linha, index, tokens) -> int:
    inicio = index
    
    while index < len(linha) and is_uppercase_letter(linha[index]):
        index += 1
        
    if not pode_terminar_token(linha, index):
        return estado_falha(linha, index, tokens, f"Palavra malformada: caractere inválido após '{linha[inicio:index]}'.")
    
    lexema = linha[inicio:index]
    
    if lexema == "RES":
        tipo = "KEYWORD_RES"
    else:
        tipo = "IDENTIFIER_MEM"
    
    retorna_token(tokens, lexema, tipo)
    return index

def estado_numero(linha, index, tokens) -> int:
    inicio = index
    
    if linha[index] == "-":
        index += 1
        if index >= len(linha) or not is_number(linha[index]):
            return estado_falha(linha, index, tokens, "Número negativo malformado: '-' deve ser seguido por um dígito.")
        
    while index < len(linha) and is_number(linha[index]):
        index += 1
        
    if index < len(linha) and linha[index] == ".":
        return estado_numero_fracionario(linha, index, inicio, tokens)
    
    if not pode_terminar_token(linha, index):
        return estado_falha(linha, index, tokens, f"Número malformado: caractere inválido após '{linha[inicio:index]}'.")
    
    lexema = linha[inicio:index]
    retorna_token(tokens, lexema, "NUMBER")
    return index

def estado_numero_fracionario(linha, index, inicio, tokens) -> int:
    #index ponto
    index += 1 
    
    if index >= len(linha) or not is_number(linha[index]): #linha fim ou não número
        return estado_falha(linha, index, tokens, "Número fracionário malformado: '.' deve ser seguido por um dígito.")
    
    while index < len(linha) and is_number(linha[index]): #não acabou e ainda é número
        index += 1
    
    if not pode_terminar_token(linha, index):
        return estado_falha(linha, index, tokens, f"Número fracionário malformado: caractere inválido após '{linha[inicio:index]}'.")
    
    lexema = linha[inicio:index]
    retorna_token(tokens, lexema, "NUMBER")
    return index

def estado_falha(linha, index, tokens, mensagem = "Erro léxico: caractere ou sequência de caracteres inválidos."):
    raise LexicalError(mensagem)


