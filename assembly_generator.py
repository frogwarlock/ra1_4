#Aluno 3 - ISABELLA LUCENA BCC 2026 - frogwarlock
#gerar_assembly e funções auxiliares
#lerArquivo está em lexer_to_assembly

import dfa

def criar_contexto_assembly():
    """
    O contexto é um dicionário que armazena informações sobre constantes, variáveis, histórico e contadores para geração de código assembly.
    """
    return {
        "constantes": {}, #valor lavel
        "variaveis":{}, # nome label
        "historico":{}, # indice linha
        "contador_constantes": 0,
        "contador_temporarios": 0,
    }
    
def registrar_constante(valor: str, contexto: dict) -> str:
    """
    Registra uma constante no contexto e retorna sua label.
    """
    constantes = contexto["constantes"]
    
    if valor in constantes:
        return constantes[valor]
    
    indice = contexto["contador_constantes"]
    label = f"CONST_{indice}"
    
    constantes[valor] = label
    contexto["contador_constantes"] += 1
    
    return label

def registrar_variavel(nome: str, contexto: dict) -> str:
    """
    Registra uma variável no contexto e retorna sua label.
    """
    variaveis = contexto["variaveis"]
    
    if nome in variaveis:
        return variaveis[nome]
    
    label = f"MEM_{nome}"
    variaveis[nome] = label
    return label

def reservar_historico(total_linhas: int, contexto: dict) -> None:
    """
    Reserva espaço no histórico para cada linha do código.
    """
    for indice_linha in range(total_linhas):
        contexto["historico"][indice_linha] = f"RES_{indice_linha}"
    
def montar_mapa_memoria(lista_linhas_tokenizadas: list[list[dfa.Token]]) -> dict:
    """
    Monta um mapa de memória com base nos tokens das linhas de código, registrando constantes, variáveis e reservando espaço para o histórico.
    """
    contexto = criar_contexto_assembly()
    
    for tokens_linha in lista_linhas_tokenizadas:
        for token in tokens_linha:
            if token.tipo == "NUMBER":
                registrar_constante(token.valor, contexto)
                
            elif token.tipo == "IDENTIFIER_MEM":
                registrar_variavel(token.valor, contexto)
                
    reservar_historico(len(lista_linhas_tokenizadas), contexto)
    return contexto

def gerarAssembly(tokens: list[dfa.Token], contexto: dict, indice_linha: int) -> list[str]:
    """
        Recebe o vetor de tokens e gera o código assembly gerado pelo analisador léxico

    Args:
        tokens (list[dfa.Token]): tokens gerados pelo analisador léxico
        codigoAssembly (list[str]): lista onde o código assembly gerado será armazenado
        contexto (dict): contexto para o assembly
        indice_linha (int): índice da linha atual
    """
    codigo_assembly = []
    tokens_linha = tokens[:]
    
    if not verifica_balanceamento_parenteses(tokens_linha):
        raise ValueError("Parênteses desbalanceados na linha")
    
    while True:
        bloco_interno = encontra_bloco_interno(tokens_linha)
        
        if bloco_interno is None:
            break
        
        indice_inicio, indice_fim, tokens_bloco = bloco_interno
        
        codigo_bloco, token_temporario = gerarAssemblyBloco(tokens_bloco, contexto, indice_linha)
        
        codigo_assembly.extend(codigo_bloco)
        
        tokens_linha = substituir_bloco_por_temporario(tokens_linha, indice_inicio, indice_fim, token_temporario)
        
    if len(tokens_linha) != 1:
        raise ValueError("Linha não reduzida para um único resultado final")
    
    token_final = tokens_linha[0]
    referencia_final = resolver_operando(token_final, contexto)
    label_res = contexto["historico"][indice_linha]
    
    codigo_assembly.extend(emitir_carrega_double(referencia_final, "R0", "D0"))
    codigo_assembly.extend(emitir_salva_double("D0", label_res, "R1"))
    
    return codigo_assembly
    


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

def encontra_bloco_interno(tokens: list[dfa.Token]) -> tuple[int, int, list[dfa.Token]]:
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

def substituir_bloco_por_temporario(tokens: list[dfa.Token], indice_inicio: int, indice_fim: int, token_temporario: dfa.Token) -> list[dfa.Token]:
    """
        Substitui o bloco de tokens entre os índices de início e fim por um token temporário, e retorna a nova lista de tokens.
    """
    return (
        tokens[:indice_inicio]
        + [token_temporario]
        + tokens[indice_fim + 1:]
    )

def resolver_operando(token: dfa.Token, contexto: dict) -> str:
    """
        Resolve o valor de um operando, seja ele uma constante, variável ou temporário, e retorna a representação adequada para o código assembly.
    """
    if token.tipo == "NUMBER":
        return registrar_constante(token.valor, contexto)
    
    elif token.tipo == "IDENTIFIER_MEM":
        return registrar_variavel(token.valor, contexto)
    
    elif token.tipo == "TEMP":
        return token.valor
    
    else:
        raise ValueError(f"Tipo de token inesperado: {token.tipo}")

def emitir_carrega_double(label: str, registrador_arm: str, registrador_vfp: str) -> list[str]:
    return [
        f"LDR {registrador_arm}, ={label}",
        f"VLDR.F64 {registrador_vfp}, [{registrador_arm}]",
    ]
    
def emitir_salva_double(registrador_vfp:str, label: str, registrador_arm: str) -> list[str]:
    return [
        f"LDR {registrador_arm}, ={label}",
        f"VSTR.F64 {registrador_vfp}, [{registrador_arm}]",
    ]

def gerarAssemblyBloco(tokens_bloco: list[dfa.Token], contexto: dict, indice_linha: int) -> tuple[list[str], dfa.Token]:
    """
        descobre qual tipo de bloco é e manda para a função correspondente, recebe a list pronta para ser adicionada ao código assembly final
    """
    if len(tokens_bloco) == 0:
        raise ValueError("Bloco vazio encontrado")
    
    # (MEM)
    if (len(tokens_bloco) == 1 and tokens_bloco[0].tipo == "IDENTIFIER_MEM"):
        return gerarAssemblyLeituraMemoria(tokens_bloco, contexto, indice_linha)

    # (V MEM)
    if (
        len(tokens_bloco) == 2 and
        tokens_bloco[0].tipo == "NUMBER"
        and tokens_bloco[1].tipo == "IDENTIFIER_MEM"
    ):
        return gerarAssemblyEscritaMemoria(tokens_bloco, contexto, indice_linha)
    
    # (N RES)
    if (
        len(tokens_bloco) == 2 and
        tokens_bloco[0].tipo == "NUMBER"
        and tokens_bloco[1].tipo == "KEYWORD_RES"
    ):
        return gerarAssemblyRES(tokens_bloco, contexto, indice_linha)
    
    # aritmético
    return gerarAssemblyAritmetico(tokens_bloco, contexto, indice_linha)

def gerarAssemblyAritmetico(tokens_bloco: list[dfa.Token], contexto: dict, indice_linha: int) -> tuple[list[str], dfa.Token]:
    pilha_operandos = []
    codigo_bloco = []
    
    for token in tokens_bloco:
        if token.tipo in {"NUMBER", "IDENTIFIER_MEM", "TEMP"}:
            referencia = resolver_operando(token, contexto)
            pilha_operandos.append(referencia)
            continue
        
        if token.tipo in {
            "ADDITION_OPERATOR",
            "SUBTRACTION_OPERATOR",
            "MULTIPLICATION_OPERATOR",
            "DIVISION_OPERATOR",
            "INTEGER_DIVISION_OPERATOR",
            "MODULO_OPERATOR",
            "EXPONENTIATION_OPERATOR",
        }:
            if len(pilha_operandos) < 2:
                raise ValueError(f"Pilha insuficiente para operação {token.valor}")
            
            operando_b = pilha_operandos.pop()
            operando_a = pilha_operandos.pop()
            
            token_temporario = criar_token_temporario(contexto)
            nome_temp = token_temporario.valor
            operacao = nome_operacao(token.tipo)
            
            if operacao_direta(token.tipo):
                codigo_bloco.extend(gerar_bloco_operacao_direta(operacao, operando_a, operando_b, nome_temp))
            else:
                codigo_bloco.extend(gerar_bloco_operacao_funcao(operacao, operando_a, operando_b, nome_temp))
            
            pilha_operandos.append(nome_temp)
            continue
        
        raise ValueError(f"Token inesperado no bloco aritmético: {token.tipo}")
    
    if len(pilha_operandos) != 1:
        raise ValueError("Bloco aritmético não reduzido a um único operando")
    
    resultado_final = pilha_operandos.pop()
    
    if not resultado_final.startswith("TEMP_"):
        token_temporario = criar_token_temporario(contexto)
        codigo_bloco.extend(emitir_carrega_double(resultado_final, "R0", "D0"))
        codigo_bloco.extend(emitir_salva_double("D0", token_temporario.valor, "R1"))
        return codigo_bloco, token_temporario
    
    return codigo_bloco, dfa.Token(tipo="TEMP", valor=resultado_final)
    
def gerarAssemblyLeituraMemoria(tokens_bloco: list[dfa.Token], contexto: dict, indice_linha: int) -> tuple[list[str], dfa.Token]:
    token_temporario = criar_token_temporario(contexto)
    nome_memoria = tokens_bloco[0].valor
    label_memoria = registrar_variavel(nome_memoria, contexto)
    
    codigo_bloco = [f"@ leitura memoria {label_memoria}"]
    codigo_bloco.extend(emitir_carrega_double(label_memoria, "R0", "D0"))
    codigo_bloco.extend(emitir_salva_double("D0", token_temporario.valor, "R1"))    
    
    return codigo_bloco, token_temporario

def gerarAssemblyEscritaMemoria(tokens_bloco: list[dfa.Token], contexto: dict, indice_linha: int) -> tuple[list[str], dfa.Token]:
    token_temporario = criar_token_temporario(contexto)
    valor_token = tokens_bloco[0]
    nome_memoria = tokens_bloco[1].valor
    
    origem = resolver_operando(valor_token, contexto)
    destino = registrar_variavel(nome_memoria, contexto)
    
    codigo_bloco = [f"@ escrita memoria {destino}"]
    codigo_bloco.extend(emitir_carrega_double(origem, "R0", "D0"))
    codigo_bloco.extend(emitir_salva_double("D0", destino, "R1"))
    codigo_bloco.extend(emitir_salva_double("D0", token_temporario.valor, "R2"))

    return codigo_bloco, token_temporario

def gerarAssemblyRES(tokens_bloco: list[dfa.Token], contexto: dict, indice_linha: int) -> tuple[list[str], dfa.Token]:
    token_temporario = criar_token_temporario(contexto)
    deslocamento = int(float(tokens_bloco[0].valor))
    
    indice_res = indice_linha - (deslocamento + 1)
    if indice_res < 0:
        raise ValueError(f"Deslocamento RES inválido: {deslocamento} para linha {indice_linha}")
    
    label_res = contexto["historico"][indice_res]
    
    codigo_bloco = [f"@ RES leitura de histórico linha {label_res}"]
    codigo_bloco.extend(emitir_carrega_double(label_res, "R0", "D0"))
    codigo_bloco.extend(emitir_salva_double("D0", token_temporario.valor, "R1"))
    
    return codigo_bloco, token_temporario

def criar_token_temporario(contexto: dict) -> dfa.Token:
    indice = contexto["contador_temporarios"]
    nome_temporario = f"TEMP_{indice}"
    contexto["contador_temporarios"] += 1
    return dfa.Token(tipo="TEMP", valor=nome_temporario)

def operacao_direta(tipo_operador: str) -> bool:
    return tipo_operador in {
        "ADDITION_OPERATOR",
        "SUBTRACTION_OPERATOR",
        "MULTIPLICATION_OPERATOR",
        "DIVISION_OPERATOR",
    }
    
def nome_operacao(tipo_operador: str) -> str:
    mapa_operacoes = {
        "ADDITION_OPERATOR": "VADD.F64",
        "SUBTRACTION_OPERATOR": "VSUB.F64",
        "MULTIPLICATION_OPERATOR": "VMUL.F64",
        "DIVISION_OPERATOR": "VDIV.F64",
        "INTEGER_DIVISION_OPERATOR": "INTEGER_DIV_64",
        "MODULO_OPERATOR": "MODULO_64",
        "EXPONENTIATION_OPERATOR": "EXPONENTIATION_64",
    }
    
    if tipo_operador not in mapa_operacoes:
        raise ValueError(f"Operador desconhecido: {tipo_operador}")
    
    return mapa_operacoes[tipo_operador]

def gerar_bloco_operacao_direta(operacao: str, operando_a: str, operando_b: str, destino: str) -> list [str]:
    codigo = [f"@ operacao {operacao}"]
    
    codigo.extend(emitir_carrega_double(operando_a, "R0", "D0"))
    codigo.extend(emitir_carrega_double(operando_b, "R1", "D1"))
    codigo.append(f"{operacao} D0, D0, D1")
    codigo.extend(emitir_salva_double("D0", destino, "R2"))
    
    return codigo
    
def gerar_bloco_operacao_funcao(nome_funcao: str, operando_a: str, operando_b: str, destino: str) -> list [str]:
    codigo = [f"@ operacao {nome_funcao} chama funcao"]
    
    codigo.extend(emitir_carrega_double(operando_a, "R0", "D0"))
    codigo.extend(emitir_carrega_double(operando_b, "R1", "D1"))
    codigo.append(f"BL {nome_funcao}")
    codigo.extend(emitir_salva_double("D0", destino, "R2"))
    
    return codigo

def gerar_secao_dados(contexto: dict) -> list[str]:
    codigo_dados = [".data"]

    # doubles auxiliares
    codigo_dados.append(".balign 8")
    codigo_dados.append("AUX_ZERO: .double 0.0")

    codigo_dados.append(".balign 8")
    codigo_dados.append("AUX_ONE: .double 1.0")

    codigo_dados.append(".balign 8")
    codigo_dados.append("AUX_TEN: .double 10.0")

    codigo_dados.append(".balign 8")
    codigo_dados.append("TMP_Q: .double 0.0")

    codigo_dados.append(".balign 8")
    codigo_dados.append("TMP_A: .double 0.0")

    codigo_dados.append(".balign 8")
    codigo_dados.append("TMP_B: .double 0.0")

    codigo_dados.append(".balign 8")
    codigo_dados.append("TMP_BASE: .double 0.0")

    codigo_dados.append(".balign 8")
    codigo_dados.append("TMP_RES: .double 0.0")

    # words auxiliares
    codigo_dados.append(".balign 4")
    codigo_dados.append("TMP_EXP_I: .word 0")

    codigo_dados.append(".balign 4")
    codigo_dados.append("AUX_INTBUF: .word 0")

    # constantes do programa
    for valor, label in contexto["constantes"].items():
        codigo_dados.append(".balign 8")
        codigo_dados.append(f"{label}: .double {valor}")

    # variáveis de memória
    for _, label in contexto["variaveis"].items():
        codigo_dados.append(".balign 8")
        codigo_dados.append(f"{label}: .double 0.0")

    # histórico
    for _, label in contexto["historico"].items():
        codigo_dados.append(".balign 8")
        codigo_dados.append(f"{label}: .double 0.0")

    # temporários
    for indice in range(contexto["contador_temporarios"]):
        codigo_dados.append(".balign 8")
        codigo_dados.append(f"TEMP_{indice}: .double 0.0")

    # tabela de segmentos por último
    codigo_dados.append("SEG_TAB: .byte 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F")

    return codigo_dados

def gerar_rotinas_auxiliares():
    codigo = []
    codigo.extend(gerar_rotina_integer_div_64())
    codigo.extend(gerar_rotina_modulo_64())
    codigo.extend(gerar_rotina_exponentiation_64())
    codigo.extend(gerar_rotina_get_seg_digit())
    codigo.extend(gerar_rotina_divmod10_u32())
    codigo.extend(gerar_rotina_display_result_7seg_1dp())
    return codigo

def gerar_rotina_integer_div_64() -> list[str]:
    return [
        "",
        "@ ===== ROTINA INTEGER_DIV_64 =====",
        "INTEGER_DIV_64:",
        "    @ entrada: D0 = A, D1 = B",
        "    @ saida:   D0 = A // B",
        "",
        "    @ se B == 0.0, retorna 0.0",
        "    VCMP.F64 D1, #0.0",
        "    VMRS APSR_nzcv, FPSCR",
        "    BEQ INTEGER_DIV_64_DIV_ZERO",
        "",
        "    @ q_real = A / B",
        "    VDIV.F64 D2, D0, D1",
        "",
        "    @ q_trunc_i = trunc(q_real) em inteiro assinado",
        "    VCVT.S32.F64 S6, D2",
        "",
        "    @ q_trunc = double(q_trunc_i)",
        "    VCVT.F64.S32 D3, S6",
        "",
        "    @ se q_real == q_trunc, terminou",
        "    VCMP.F64 D2, D3",
        "    VMRS APSR_nzcv, FPSCR",
        "    BEQ INTEGER_DIV_64_DONE",
        "",
        "    @ se q_real >= 0, truncamento ja coincide com floor",
        "    VCMP.F64 D2, #0.0",
        "    VMRS APSR_nzcv, FPSCR",
        "    BGE INTEGER_DIV_64_DONE",
        "",
        "    @ caso negativo com parte fracionaria: floor = trunc - 1.0",
        "    LDR R0, =AUX_ONE",
        "    VLDR.F64 D4, [R0]",
        "    VSUB.F64 D3, D3, D4",
        "",
        "INTEGER_DIV_64_DONE:",
        "    LDR R0, =TMP_Q",
        "    VSTR.F64 D3, [R0]",
        "    VLDR.F64 D0, [R0]",
        "    BX LR",
        "",
        "INTEGER_DIV_64_DIV_ZERO:",
        "    LDR R0, =AUX_ZERO",
        "    VLDR.F64 D0, [R0]",
        "    BX LR",
    ]


def gerar_rotina_modulo_64() -> list[str]:
    return [
        "",
        "@ ===== ROTINA MODULO_64 =====",
        "MODULO_64:",
        "    @ entrada: D0 = A, D1 = B",
        "    @ saida:   D0 = A % B",
        "",
        "    PUSH {LR}",
        "",
        "    @ se B == 0.0, retorna 0.0",
        "    VCMP.F64 D1, #0.0",
        "    VMRS APSR_nzcv, FPSCR",
        "    BEQ MODULO_64_DIV_ZERO",
        "",
        "    @ guarda A e B em memoria",
        "    LDR R0, =TMP_A",
        "    VSTR.F64 D0, [R0]",
        "    LDR R0, =TMP_B",
        "    VSTR.F64 D1, [R0]",
        "",
        "    @ q = A // B",
        "    BL INTEGER_DIV_64",
        "",
        "    @ recarrega B",
        "    LDR R0, =TMP_B",
        "    VLDR.F64 D7, [R0]",
        "",
        "    @ D2 = q * B",
        "    VMUL.F64 D2, D0, D7",
        "",
        "    @ recarrega A",
        "    LDR R0, =TMP_A",
        "    VLDR.F64 D6, [R0]",
        "",
        "    @ r = A - q * B",
        "    VSUB.F64 D0, D6, D2",
        "",
        "    POP {LR}",
        "    BX LR",
        "",
        "MODULO_64_DIV_ZERO:",
        "    LDR R0, =AUX_ZERO",
        "    VLDR.F64 D0, [R0]",
        "    POP {LR}",
        "    BX LR",
    ]


def gerar_rotina_exponentiation_64() -> list[str]:
    return [
        "",
        "@ ===== ROTINA EXPONENTIATION_64 =====",
        "EXPONENTIATION_64:",
        "    @ entrada: D0 = base, D1 = expoente",
        "    @ saida:   D0 = base ^ expoente",
        "    @ esta versao aceita apenas expoente inteiro nao negativo",
        "",
        "    @ se expoente < 0.0, retorna 0.0",
        "    VCMP.F64 D1, #0.0",
        "    VMRS APSR_nzcv, FPSCR",
        "    BLT EXPONENTIATION_64_INVALID",
        "",
        "    @ converte expoente para inteiro truncado",
        "    VCVT.S32.F64 S8, D1",
        "    VCVT.F64.S32 D3, S8",
        "",
        "    @ se expoente original != expoente inteiro, invalido",
        "    VCMP.F64 D1, D3",
        "    VMRS APSR_nzcv, FPSCR",
        "    BNE EXPONENTIATION_64_INVALID",
        "",
        "    @ move contador inteiro para registrador ARM via memoria",
        "    LDR R0, =TMP_EXP_I",
        "    VSTR S8, [R0]",
        "    LDR R4, [R0]",
        "",
        "    @ resultado = 1.0",
        "    LDR R0, =AUX_ONE",
        "    VLDR.F64 D4, [R0]",
        "",
        "    @ guarda base via memoria",
        "    LDR R0, =TMP_BASE",
        "    VSTR.F64 D0, [R0]",
        "    VLDR.F64 D5, [R0]",
        "",
        "EXPONENTIATION_64_LOOP_CHECK:",
        "    CMP R4, #0",
        "    BEQ EXPONENTIATION_64_DONE",
        "",
        "    VMUL.F64 D4, D4, D5",
        "    SUB R4, R4, #1",
        "    B EXPONENTIATION_64_LOOP_CHECK",
        "",
        "EXPONENTIATION_64_DONE:",
        "    LDR R0, =TMP_RES",
        "    VSTR.F64 D4, [R0]",
        "    VLDR.F64 D0, [R0]",
        "    BX LR",
        "",
        "EXPONENTIATION_64_INVALID:",
        "    LDR R0, =AUX_ZERO",
        "    VLDR.F64 D0, [R0]",
        "    BX LR",
    ]
    
# seven segment 
def gerar_rotina_get_seg_digit() -> list[str]:
    return [
        "",
        "@ ===== ROTINA GET_SEG_DIGIT =====",
        "GET_SEG_DIGIT:",
        "    @ entrada: R0 = digito (0..9)",
        "    @ saida:   R0 = padrao do 7 segmentos",
        "    PUSH {R1, LR}",
        "    LDR R1, =SEG_TAB",
        "    LDRB R0, [R1, R0]",
        "    POP {R1, LR}",
        "    BX LR",
    ]


def gerar_rotina_divmod10_u32() -> list[str]:
    return [
        "",
        "@ ===== ROTINA DIVMOD10_U32 =====",
        "DIVMOD10_U32:",
        "    @ entrada: R0 = valor",
        "    @ saida:   R0 = quociente, R1 = resto",
        "    PUSH {R2, LR}",
        "    MOV R2, #0",
        "",
        "DIVMOD10_U32_LOOP:",
        "    CMP R0, #10",
        "    BLT DIVMOD10_U32_DONE",
        "    SUB R0, R0, #10",
        "    ADD R2, R2, #1",
        "    B DIVMOD10_U32_LOOP",
        "",
        "DIVMOD10_U32_DONE:",
        "    MOV R1, R0",
        "    MOV R0, R2",
        "    POP {R2, LR}",
        "    BX LR",
    ]


def gerar_rotina_display_result_7seg_1dp() -> list[str]:
    return [
        "",
        "@ ===== ROTINA DISPLAY_RESULT_7SEG_1DP =====",
        "DISPLAY_RESULT_7SEG_1DP:",
        "    @ entrada: D0 = valor final",
        "    PUSH {R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, LR}",
        "",
        "    @ sinal",
        "    MOV R9, #0",
        "    VCMP.F64 D0, #0.0",
        "    VMRS APSR_nzcv, FPSCR",
        "    BGE DISPLAY_RESULT_7SEG_POSITIVE",
        "    MOV R9, #0x40",
        "    VNEG.F64 D0, D0",
        "",
        "DISPLAY_RESULT_7SEG_POSITIVE:",
        "    @ escala por 10",
        "    LDR R0, =AUX_TEN",
        "    VLDR.F64 D1, [R0]",
        "    VMUL.F64 D0, D0, D1",
        "",
        "    @ converte para inteiro",
        "    VCVT.U32.F64 S0, D0",
        "    LDR R0, =AUX_INTBUF",
        "    VSTR S0, [R0]",
        "    LDR R4, [R0]",
        "",
        "    @ separa parte inteira e decimal",
        "    MOV R0, R4",
        "    BL DIVMOD10_U32",
        "    MOV R5, R0      @ parte inteira",
        "    MOV R6, R1      @ decimal",
        "",
        "    @ separa unidades, dezenas e centenas",
        "    MOV R0, R5",
        "    BL DIVMOD10_U32",
        "    MOV R5, R1      @ unidades",
        "    MOV R7, R0      @ dezenas+centenas",
        "",
        "    MOV R0, R7",
        "    BL DIVMOD10_U32",
        "    MOV R8, R1      @ dezenas",
        "    MOV R7, R0      @ centenas",
        "",
        "    @ converte decimal",
        "    MOV R0, R6",
        "    BL GET_SEG_DIGIT",
        "    MOV R6, R0",
        "",
        "    @ converte unidades (sempre mostra)",
        "    MOV R0, R5",
        "    BL GET_SEG_DIGIT",
        "    MOV R5, R0",
        "",
        "    @ converte dezenas:",
        "    @ mostra se centenas != 0 OU dezenas != 0",
        "    CMP R7, #0",
        "    BNE DISPLAY_RESULT_7SEG_SHOW_TENS",
        "    CMP R8, #0",
        "    BNE DISPLAY_RESULT_7SEG_SHOW_TENS",
        "    MOV R8, #0",
        "    B DISPLAY_RESULT_7SEG_TENS_DONE",
        "",
        "DISPLAY_RESULT_7SEG_SHOW_TENS:",
        "    MOV R0, R8",
        "    BL GET_SEG_DIGIT",
        "    MOV R8, R0",
        "",
        "DISPLAY_RESULT_7SEG_TENS_DONE:",
        "    @ converte centenas ou deixa branco",
        "    CMP R7, #0",
        "    BEQ DISPLAY_RESULT_7SEG_HUNDREDS_BLANK",
        "    MOV R0, R7",
        "    BL GET_SEG_DIGIT",
        "    MOV R7, R0",
        "    B DISPLAY_RESULT_7SEG_HUNDREDS_DONE",
        "",
        "DISPLAY_RESULT_7SEG_HUNDREDS_BLANK:",
        "    MOV R7, #0",
        "",
        "DISPLAY_RESULT_7SEG_HUNDREDS_DONE:",
        "    @ monta HEX3..HEX0 = dezenas, unidades, _, decimal",
        "    MOV R0, R6",
        "    ORR R0, R0, #0x00000800",
        "    ORR R0, R0, R5, LSL #16",
        "    ORR R0, R0, R8, LSL #24",
        "",
        "    LDR R1, =0xFF200020",
        "    STR R0, [R1]",
        "",
        "    @ monta HEX5..HEX4 = sinal, centenas",
        "    MOV R0, R7",
        "    ORR R0, R0, R9, LSL #8",
        "",
        "    LDR R1, =0xFF200030",
        "    STR R0, [R1]",
        "",
        "    POP {R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, LR}",
        "    BX LR",
    ]