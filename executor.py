# funções referentes ao aluno 2
from dfa import Token

def criar_token_numero(valor:float) -> Token:
    return Token(tipo="NUMBER", valor=str(valor), memoria=8)

def executarExpressao(tokens: list, memoria: dict, historico: list) -> float:
    """
        Função principal para execução de expressões. Recebe uma lista de tokens, o estado atual da memória e o histórico de resultados.
        Retorna o resultado da expressão avaliada.
        - verifica balanceamento
        - encontra blocos internos 
        - reduz bloco para resultados
        - salva resultado em memória ou histórico se necessário
    """
    tokens_linha = tokens[:]
    
    if not verifica_balanceamento_parenteses(tokens_linha):
        raise ValueError("Parênteses não estão balanceados")
    
    while True:
        bloco_interno = encontra_bloco_interno(tokens_linha)
        
        if bloco_interno is None:
            break # Não achou, acabou.
        
        inicio, fim, tokens_bloco = bloco_interno
        resultado_bloco = avalia_bloco(tokens_bloco, memoria, historico)
        tokens_linha = substituir_bloco_por_resultado(tokens_linha, inicio, fim, resultado_bloco)
        
    if len(tokens_linha) != 1:
        raise ValueError(
                         f"A expressão não foi reduzida corretamente. Tokens restantes: {[token.valor for token in tokens_linha]}")
    
    if tokens_linha[0].tipo != "NUMBER":
        raise ValueError(f"O resultado final não é um número. Token final: {tokens_linha[0]}")
    
    resultado_final = float(tokens_linha[0].valor)
    historico.append(resultado_final)
    return resultado_final

def verifica_balanceamento_parenteses(tokens: list) -> bool:
    """"
        Única checagem sintática da Fase 1:
        Verificar se os parênteses estão balanceados (cada parêntese aberto tem um correspondente fechado).
    """
    pilha_parenteses_abertos = []
    
    for caractere in tokens:
       if caractere.valor == "(":
              pilha_parenteses_abertos.append(caractere)
              
       elif caractere.valor == ")":
            if not pilha_parenteses_abertos:
                return False  # Encontrou um parêntese fechado sem um correspondente aberto
            
            pilha_parenteses_abertos.pop()
            
    return len(pilha_parenteses_abertos) == 0  # Verifica se todos os parênteses abertos foram fechados

def encontra_bloco_interno(tokens: list) -> list:
    """
        Encontra o bloco mais interno entre parênteses.
        Retorna:
            (indice_abertura, indice_fechamento, tokens_internos)
        ou None se não houver blocos internos.
    """
    
    pilha_aberturas = []
    for index, token in enumerate(tokens):
        if token.tipo == "PARENTHESIS":
            if token.valor == "(":
                pilha_aberturas.append(index)
            
            elif token.valor == ")":
                if not pilha_aberturas:
                    raise ValueError("Parêntese de fehamento sem abertura correspondente")
                
                inicio = pilha_aberturas.pop()
                fim = index
                tokens_internos = tokens[inicio + 1 : fim]
                return (inicio, fim, tokens_internos)
    
    return None  # Não encontrou blocos internos

def avalia_bloco(tokens_bloco: list, memoria: dict, historico: list): #sem type hint pq não sei o que retorna ainda
    """
        Decide o tipo de bloco:
            - Leitura memória (MEM)
            - Escrita memória (V MEM)
            - Histórico (N RES)
            - Aritmético 
    """
    if len(tokens_bloco) == 0:
        raise ValueError("Bloco vazio não pode ser avaliado")
    
    # (MEM)
    if len(tokens_bloco) == 1 and tokens_bloco[0].tipo == "IDENTIFIER_MEM":
        return avalia_leitura_memoria(tokens_bloco, memoria)
    
    # (V MEM)
    if (len(tokens_bloco) == 2 
        and tokens_bloco[0].tipo == "NUMBER"
        and tokens_bloco[1].tipo == "IDENTIFIER_MEM"
        ):
        return avalia_escrita_memoria(tokens_bloco, memoria)
    
    # (N RES)
    if (len(tokens_bloco) == 2
        and tokens_bloco[0].tipo == "NUMBER"
        and tokens_bloco[1].tipo == "KEYWORD_RES"
         ):
        return avalia_historico_res(tokens_bloco, historico)
    
    # aritmético
    return avalia_bloco_aritmetico(tokens_bloco, memoria, historico)

def substituir_bloco_por_resultado(tokens: list, inicio: int, fim: int, resultado: float) -> list:
    """
        Substitui o bloco entre os índices inicio e fim por um token do resultado.
    """
    token_resultado = criar_token_numero(resultado)
    return tokens[:inicio] + [token_resultado] + tokens[fim + 1 :]

def avalia_leitura_memoria(tokens_bloco: list, memoria:dict) -> float:
    """
        Avalia um bloco de leitura de memória (MEM). Exemplo: (MEM)
        Retorna o valor armazenado na memória para o nome especificado.
    """
    nome_memoria = tokens_bloco[0].valor
    return float(memoria.get(nome_memoria, 0.0))

def avalia_escrita_memoria(tokens_bloco: list, memoria: dict) -> float:
    """
        Avalia um bloco de escrita de memória (V MEM). Exemplo: (5 MEM)
        Escreve o valor especificado na memória para o nome dado e retorna o valor escrito
    """
    valor = float(tokens_bloco[0].valor)
    nome_memoria = tokens_bloco[1].valor
    
    memoria[nome_memoria] = valor
    return valor

def avalia_historico_res(tokens_bloco: list, historico: list) -> float:
    """
        Avalia um bloco de histórico (N RES). Exemplo: (0 RES)
        Retorna o valor armazenado no histórico para o índice especificado.
    """

    index_historico = float(tokens_bloco[0].valor)
    
    if not index_historico.is_integer() or index_historico < 0:
        raise ValueError(f"Índice de histórico inválido: {index_historico}. Deve ser um número inteiro não negativo.")
    
    index_historico = int(index_historico)
    
    if index_historico >= len(historico):
        raise ValueError(f"Índice de histórico fora do alcance: {index_historico}. Histórico atual tem {len(historico)} entradas.")
    
    return float(historico[-(index_historico + 1)])

def avalia_bloco_aritmetico(tokens_bloco: list, memoria: dict, historico: list):
    pilha = []
    
    for token in tokens_bloco:
        if token.tipo == "NUMBER":
            pilha.append(float(token.valor))
            continue
            
        elif token.tipo == "IDENTIFIER_MEM":
            nome_memoria = token.valor
            pilha.append(float(memoria.get(nome_memoria, 0.0)))
            continue
        
        if token.tipo in {
            "ADDITION_OPERATOR",
            "SUBTRACTION_OPERATOR",
            "MULTIPLICATION_OPERATOR",
            "DIVISION_OPERATOR",
            "INTEGER_DIVISION_OPERATOR",
            "MODULO_OPERATOR",
            "EXPONENTIATION_OPERATOR"
        }:
            if len(pilha) < 2:
                raise ValueError(
                    f"Pilha insuficiente para operação '{token.valor}'. Pilha atual: {pilha}"
                )
                
            b = pilha.pop()
            a = pilha.pop()
            resultado = aplica_operador(a, b, token.tipo)
            pilha.append(resultado)
            continue
        
        raise ValueError(f"Token inesperado em bloco aritmético: {token}")
    
    if len(pilha) != 1:
        raise ValueError(f"Bloco aritmético não foi reduzido a um único resultado. Pilha final: {pilha}")
    
    return pilha[0]

def aplica_operador(a:float, b:float, tipo_operador:str) -> float:
    if tipo_operador == "ADDITION_OPERATOR":
        return a + b
    
    if tipo_operador == "SUBTRACTION_OPERATOR":
        return a - b
    
    if tipo_operador == "MULTIPLICATION_OPERATOR":
        return a * b
    
    if tipo_operador == "DIVISION_OPERATOR":
        if b == 0:
            raise ValueError("Divisão por zero.")
        return a / b
    
    if tipo_operador == "INTEGER_DIVISION_OPERATOR":
        if b == 0:
            raise ValueError("Divisão inteira por zero.")
        return a // b
    
    if tipo_operador == "MODULO_OPERATOR":
        if b == 0:
            raise ValueError("Módulo por zero.")
        return a % b
    
    if tipo_operador == "EXPONENTIATION_OPERATOR":
        return a ** b
    
    raise ValueError(f"Tipo de operador desconhecido: {tipo_operador}")
                

