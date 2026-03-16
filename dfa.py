#maquina de estados finitos 
# Implementação do Analisador léxico usando Autômatos Finitos Determinísticos (AFDs), com cada estado como uma função.

class LexicalError(Exception):
    pass

ESPACOS = {" ", "\t"}
OPERADORES_SIMPLES = {"+", "*", "%", "ˆ"}
PARENTESES = {"(", ")"}

def is_number(caractere: str) -> bool:
    return "0" <= caractere <= "9"

def is_uppercase_letter(caractere: str) -> bool:
    return "A" <= caractere <= "Z"

def retorna_token(tokens: list[str], lexema: str):
    tokens.append(lexema)
    
def is_DVT_eD_eP(linha: str, index: int) -> bool:
    """
    Delimitador Valido de Token para encerrar o estado Digito e estadp Palavra
    """
    
    if index >= len(linha): #fim de linha é um delimitador válido
        return True  
    
    caractere = linha[index]
    return caractere in ESPACOS or caractere in PARENTESES

def is_DVT_eO(linha: str, index: int) -> bool:
    """
    Delimitador Valido de Token para encerrar o estado Operador
    """
    
    if index >= len(linha):
        return True  
    
    caractere = linha[index]
    return caractere in ESPACOS or caractere in PARENTESES


def estado_inicial(linha, index, tokens):
    """
    Estado inicial é responsável analisar o caractere atual e decidir qual estado seguir com base no tipo do caractere (número, letra, operador, etc.).
    Args:
        linha (list): A linha de código a ser analisada
        index (int): O índice atual na linha
        tokens (list): A lista de tokens encontrados até o momento
    """
    caractere = linha[index]
    
    if caractere in ESPACOS:
        return index + 1  #ignora espaço em branco e vai para o próximo
    
    if is_number(caractere):
        return estado_numero(linha, index, tokens)
    
    if caractere == "-":
        return estado_intermediario(linha, index, tokens)
    
    if caractere in OPERADORES_SIMPLES or caractere == "/":
        return estado_operador(linha, index, tokens)
    
    if is_uppercase_letter(caractere):
        return estado_palavra(linha, index, tokens)
    
    if caractere in PARENTESES:
        return estado_parenteses(linha, index, tokens)
    
    return estado_falha(linha, index, tokens, f"Caractere inválido: '{caractere}' no índice {index}")

def estado_intermediario(linha, index, tokens):
    """
    Estado intermediário para lidar com o operador de subtração '-' que pode ser um operador ou parte de um número negativo.
    """
    proximo = index + 1
    
    if proximo < len(linha) and is_number(linha[proximo]):
        return estado_numero(linha, index, tokens)  # Trata como número negativo
    
    return estado_operador(linha, index, tokens)  # Trata como operador de subtração
      
def estado_parenteses(linha, index, tokens):
    """
    Estado responsável por reconhecer parênteses sem validar o balance.
    """
    
    caractere = linha[index]
    
    if caractere == "(" or caractere == ")":
        retorna_token(tokens, caractere)
        return index + 1
    
    return estado_falha(linha, index, tokens, f"Caractere inválido: '{caractere}' no índice {index}")
    
def estado_operador(linha, index, tokens):
    caractere = linha[index]
    #operadores de um caractere
    if caractere in OPERADORES_SIMPLES or caractere == "-":
        proximo_index = index + 1
        
        if not is_DVT_eO(linha, proximo_index):
            return estado_falha(linha, index, tokens, f"Operador '{caractere}' deve ser seguido por um delimitador válido.")
        
        retorna_token(tokens, caractere)
        return proximo_index
    
    #caso / ou //
    if caractere == "/":
        proximo_index = index + 1
        
        if proximo_index < len(linha) and linha[proximo_index] == "/":
            fim = proximo_index + 1
            
            if not is_DVT_eO(linha, fim):
                return estado_falha(linha, index, tokens, "Operador '//' deve ser seguido por um delimitador válido.")
            retorna_token(tokens, "//")
            return fim
        
        if not is_DVT_eO(linha, proximo_index):
            return estado_falha(linha, index, tokens, "Operador '/' deve ser seguido por um delimitador válido.")
        retorna_token(tokens, "/")
        return proximo_index
    
    return estado_falha(linha, index, tokens, f"Caractere '{caractere}' não é um operador válido.")

def estado_palavra(linha, index, tokens):
    inicio = index
    
    while index < len(linha) and is_uppercase_letter(linha[index]):
        index += 1
        
    if not is_DVT_eD_eP(linha, index):
        return estado_falha(linha, index, tokens, f"Palavra malformada: caractere inválido após '{linha[inicio:index]}'.")
    
    lexema = linha[inicio:index]
    retorna_token(tokens, lexema)
    return index

def estado_numero(linha, index, tokens):
    inicio = index
    
    if linha[index] == "-":  # Lida com número negativo
        index += 1
        if index >= len(linha) or not is_number(linha[index]):
            return estado_falha(linha, index, tokens, "Número negativo malformado: '-' deve ser seguido por um dígito.")
        
        #parte inteira
    while index < len(linha) and is_number(linha[index]):
        index += 1
        
    #parte decimal
    if index < len(linha) and linha[index] == ".":
        index += 1
        if index >= len(linha) or not is_number(linha[index]):
            return estado_falha(linha, index, tokens, "Número decimal malformado: '.' deve ser seguido por pelo menos um dígito.")
        
        while index < len(linha) and is_number(linha[index]):
            index += 1
            
    if not is_DVT_eD_eP(linha, index):
        return estado_falha(linha, index, tokens, f"Número malformado: caractere inválido após '{linha[inicio:index]}'.")
    
    lexema = linha[inicio:index]
    retorna_token(tokens, lexema)
    return index

def estado_falha(linha, index, tokens, mensagem = "Erro léxico: caractere ou sequência de caracteres inválidos."):
    raise LexicalError(mensagem)


