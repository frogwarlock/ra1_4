#Aluno 3 
#gerar_assembly e funções auxiliares
#lerArquivo está em lexer_to_assembly

import dfa

contador_temporarios = 0

def gerarAssembly(tokens: list[dfa.Token]) -> list[str]:
    """
        Recebe o vetor de tokens e gera o código assembly gerado pelo analisador léxico

    Args:
        tokens (list[dfa.Token]): tokens gerados pelo analisador léxico
        codigoAssembly (list[str]): lista onde o código assembly gerado será armazenado
    """
    codigoAssembly = []
    tokens_linha = tokens[:]
    
    if not verifica_balanceamento_parenteses(tokens_linha):
        raise ValueError("Parênteses não estão balanceados")
    
    while True:
        bloco_interno = encontra_bloco_interno(tokens_linha)
        
        if bloco_interno is None:
            break
        
        indice_inicio, indice_fim, tokens_bloco = bloco_interno
        
        codigo_bloco, token_temporario = gerarAssemblyBloco(tokens_bloco)
        
        codigoAssembly.extend(codigo_bloco)
        
        tokens_linha = substituir_bloco_por_temporario(
            tokens_linha,
            indice_inicio,
            indice_fim,
            token_temporario
        )
        
    return codigoAssembly


def  verifica_balanceamento_parenteses(tokens: list[dfa.Token]) -> bool:
    pilha_parentesis_aberto = []
    
    for token in tokens:
        if token.valor == "(":
            pilha_parentesis_aberto.append(token)
        elif token.valor == ")":
            if not pilha_parentesis_aberto:
                return False
            
            pilha_parentesis_aberto.pop()
            
    return len(pilha_parentesis_aberto) == 0

def encontra_bloco_interno(tokens: list[dfa.Token]) -> None:
    """
        Encontra o bloco mais interno de parênteses e retorna os índices de início e fim, além dos tokens contidos nesse bloco.
        Se não houver blocos de parênteses, retorna None.
    """
    pilha_abertura = []
    for index, token in enumerate(tokens):
        if token.valor == "(":
            pilha_abertura.append(index)
            
        elif token.valor == ")":
            if not pilha_abertura:
                raise ValueError("Parêntese de fechamento sem abertura correspondente")
            
            indice_inicio = pilha_abertura.pop()
            indice_fim = index
            tokens_bloco = tokens[indice_inicio + 1:indice_fim]
            return (indice_inicio, indice_fim, tokens_bloco)
        
    return None  # Não encontrou blocos internos

def substituir_bloco_por_temporario(tokens: list[dfa.Token], indice_inicio: int, indice_fim: int, token_temporario: str) -> list[dfa.Token]:
    """
        Substitui o bloco de tokens entre os índices de início e fim por um token temporário, e retorna a nova lista de tokens.
    """
    return (
        tokens[:indice_inicio]
        + [token_temporario]
        + tokens[indice_fim + 1:]
    )

def gerarAssemblyBloco(tokens_bloco: list[dfa.Token]) -> tuple[list[str], dfa.Token]:
    """
        descobre qual tipo de bloco é e manda para a função correspondente, recebe a list pronta para ser adicionada ao código assembly final
    """
    if len(tokens_bloco) == 0:
        raise ValueError("Bloco vazio encontrado")
    
    # (MEM)
    if (len(tokens_bloco) == 1 and tokens_bloco[0].tipo == "IDENTIFIER_MEM"):
        return gerarAssemblyLeituraMemoria(tokens_bloco)

    # (V MEM)
    if (
        len(tokens_bloco) == 2 and
        tokens_bloco[0].tipo == "NUMBER"
        and tokens_bloco[1].tipo == "IDENTIFIER_MEM"
    ):
        return gerarAssemblyEscritaMemoria(tokens_bloco)
    
    # (N RES)
    if (
        len(tokens_bloco) == 2 and
        tokens_bloco[0].tipo == "NUMBER"
        and tokens_bloco[1].tipo == "KEYWORD_RES"
    ):
        return gerarAssemblyRES(tokens_bloco)
    
    # aritmético
    return gerarAssemblyAritmetico(tokens_bloco)

def gerarAssemblyAritmetico(tokens_bloco: list[dfa.Token]) -> list[str]:
    token_temporario = criar_token_temporario()
    
    valores = [token.valor for token in tokens_bloco]
    codigo_bloco = [
        f"; BLOCO ARITMÉTICO: {' '.join(valores)}",
        f"; resultado armazenado em {token_temporario.valor}",
    ]
    
    return codigo_bloco, token_temporario
    
def gerarAssemblyLeituraMemoria(tokens_bloco: list[dfa.Token]) -> list[str]:
    token_temporario = criar_token_temporario()
    nome_memoria = tokens_bloco[0].valor
    
    codigo_bloco = [
        f"; BLOCO DE LEITURA DE MEMÓRIA: {nome_memoria}",
        f"; resultado armazenado em {token_temporario.valor}"
    ]
    
    return codigo_bloco, token_temporario

def gerarAssemblyEscritaMemoria(tokens_bloco: list[dfa.Token]) -> list[str]:
    token_temporario = criar_token_temporario()
    valor = tokens_bloco[0].valor
    nome_memoria = tokens_bloco[1].valor
    
    codigo_bloco = [
        f"; ESCRITA DE MEMÓRIA: {valor} -> {nome_memoria}",
        f"; resultado armazenado em {token_temporario.valor}"
    ]
    
    return codigo_bloco, token_temporario

def gerarAssemblyRES(tokens_bloco: list[dfa.Token]) -> list[str]:
    token_temporario = criar_token_temporario()
    indice = tokens_bloco[0].valor
    
    codigo_bloco = [
        f"; BLOCO RES: {indice} RES",
        f"; resultado armazenado em {token_temporario.valor}"
    ]
    
    return codigo_bloco, token_temporario

def criar_token_temporario() -> dfa.Token:
    global contador_temporarios

    nome_temporario = f"temp{contador_temporarios}"
    contador_temporarios += 1

    return dfa.Token(tipo="TEMP", valor=nome_temporario)