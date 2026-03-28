#Isabella Lucena Conceição - frogwarlock no github
#ra1_4
import sys
import dfa
import executor
import assembly_generator

def lerArquivo(nomeArquivo: str, linhas: list[str]) -> None:
    """
        Lê arquivo de entrada e preenche a lista de linhas.
    """
    with open(nomeArquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linhas.append(linha.rstrip('\n'))

def salvar_arquivo_assembly(nome_arquivo_entrada: str, codigo_assembly: list[str]) -> None:
    """
        Salva o código assembly gerado em um arquivo de saída .s
    """
    if nome_arquivo_entrada.endswith('.txt'):
        nome_arquivo_saida = 'resultado_assembly.s'
    else:
        nome_arquivo_saida = 'resultado_assembly.s'
        
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
        for linha in codigo_assembly:
            arquivo_saida.write(linha + '\n')
            
    return nome_arquivo_saida

def salvar_arquivo_token(nome_arquivo_entrada: str, linhas_tokenizadas: list[list[dfa.Token]]) -> str:
    """
        Salva os tokens gerados em um arquivo de saída .txt
    """
    if nome_arquivo_entrada.endswith('.txt'):
        nome_arquivo_saida = 'resultado_tokens.txt'
    else:
        nome_arquivo_saida = 'resultado_tokens.txt'
        
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
        for indice_linha, tokens_linha in enumerate(linhas_tokenizadas):
            token_values = [token.valor for token in tokens_linha]
            arquivo_saida.write(f"{indice_linha + 1}: {token_values}\n")
            
    return nome_arquivo_saida

#responsável por reconhecer pedaços VÁLIDOS do código não fazer verificação da operação de expressão
def parseExpressao(linha:str) -> list[dfa.Token]:
    tokens = []
    index = 0
    while index < len(linha):
        # print(f"Analisando caractere: '{linha[index]}' no índice {index}")
        # index+= 1
        index = dfa.estado_inicial(linha,index, tokens) 
    
    return tokens

def exibirResultados(resultados: list[float]) -> None:
    """Mostra os resultados formatados"""
    print("\n")
    for indice, resultado in enumerate(resultados, start=1):
        print(f"Resultado da linha {indice}: {resultado}")


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python main.py <filename>.txt [--teste]")
        raise SystemExit(1)

    if len(sys.argv) == 3 and sys.argv[2] != "--teste":
        print("Flag inválida. Use apenas --teste")
        raise SystemExit(1)
    
    nomeArquivo = sys.argv[1]
    linhas = []
    
    try:
        lerArquivo(nomeArquivo, linhas)
    except (FileNotFoundError, OSError) as error:
        print(f"Erro ao ler o arquivo: {error}")
        raise SystemExit(1)
    
    linhas_tokenizadas = []
    
    #lexico
    for numero_linha, linha in enumerate(linhas, start=1):
        try:
            tokens = parseExpressao(linha)
            linhas_tokenizadas.append(tokens)
        except Exception as error:
            print(f"Erro lexico na linha {numero_linha}: {error}")
            raise SystemExit(1)
        
    #salva arquivo tokens
    nome_arquivo_tokens = salvar_arquivo_token(nomeArquivo, linhas_tokenizadas)
    print(f"Tokens salvos em: {nome_arquivo_tokens}")
    
    #executa exibicao de resultados
    resultados = []
    memoria = {}
    historico = []
    
    for numero_linha, tokens in enumerate(linhas_tokenizadas, start=1):
        try:
            resultado = executor.executarExpressao(tokens, memoria, historico)
            resultados.append(resultado)
        except Exception as error:
            print(f"Erro na execução da linha {numero_linha}: {error}")
            raise SystemExit(1)
        
    #so aparece se tiver subido a flag --teste   
    if len(sys.argv) == 3 and sys.argv[2] == "--teste":
        exibirResultados(resultados)
    
    #gerar assembly
    contexto = assembly_generator.montar_mapa_memoria(linhas_tokenizadas)

    codigo_texto = [
        ".syntax unified",
        "",
        ".text",
        ".global _start",
        "",
        "_start:",
    ]

    # chamada explícita da função pedida pelo professor
    for indice_linha, tokens_linha in enumerate(linhas_tokenizadas):
        codigo_texto.append(f"    @ ===== LINHA {indice_linha + 1} =====")
        codigo_linha = assembly_generator.gerarAssembly( #chamada do assembly_generator para cada linha de tokens
            tokens_linha,
            contexto,
            indice_linha
        )

        for instrucao in codigo_linha:
            if instrucao.endswith(":"):
                codigo_texto.append(instrucao)
            else:
                codigo_texto.append(f"    {instrucao}")

        codigo_texto.append("")

    ultimo_res = f"RES_{len(linhas_tokenizadas) - 1}"

    codigo_texto.extend([
        f"      LDR R0, ={ultimo_res}",
        "      VLDR.F64 D0, [R0]",
        "      BL DISPLAY_RESULT_7SEG_1DP",
        "    @ fim do programa",
        "FIM:",
        "    B FIM",
    ])

    # IMPORTANTE:
    # gerar_secao_dados deve vir depois da geração do código,
    # porque os TEMP_n só são descobertos durante gerarAssembly(...)
    codigo_dados = assembly_generator.gerar_secao_dados(contexto)
    codigo_rotinas = assembly_generator.gerar_rotinas_auxiliares()

    codigo_assembly_final = []
    codigo_assembly_final.extend(codigo_dados)
    codigo_assembly_final.extend(codigo_texto)
    codigo_assembly_final.extend(codigo_rotinas)

    nome_arquivo_assembly = salvar_arquivo_assembly(
        nomeArquivo,
        codigo_assembly_final
    )

    print(f"\nArquivo de tokens gerado: {nome_arquivo_tokens}")
    print(f"Arquivo Assembly gerado: {nome_arquivo_assembly}")

            
            
if __name__ == "__main__":
    main()