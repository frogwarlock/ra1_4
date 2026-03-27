#Isabella Lucena Conceição
#ra1_4
import sys
import dfa
import executor
import assembly_generator

#TODO O vetor de tokens gerado pelo Analisador Léxico deve ser salvo em um arquivo .txt para uso nas próximas fases do projeto.

def lerArquivo(nomeArquivo: str, linhas: list[str]) -> None:
    """
        Lê arquivo de entrada e preenche a lista de linhas.
    """
    with open(nomeArquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linhas.append(linha.rstrip('\n'))

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
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>.txt")
        raise SystemExit(1)
    
    nomeArquivo = sys.argv[1]
    linhas = []
    
    try:
        lerArquivo(nomeArquivo, linhas)
    except (FileNotFoundError, OSError) as error:
        print(f"Erro ao ler o arquivo: {error}")
        raise SystemExit(1)
    
    # memoria = {}
    # historico = []
    linhas_tokenizadas = []
    
    for numero_linha, linha in enumerate(linhas, start=1):
            tokens = parseExpressao(linha)
            # resultado = executor.executarExpressao(tokens, memoria, historico)
            linhas_tokenizadas.append(tokens)
    contexto = assembly_generator.montar_mapa_memoria(linhas_tokenizadas)
    
    for indice_linha, tokens_linha in enumerate(linhas_tokenizadas):
        gerar_codigo_assembly = assembly_generator.gerarAssembly(tokens_linha, contexto, indice_linha)

        print(f"Tokens na linha {indice_linha + 1}: {[token.valor for token in tokens_linha]}")
        print(f"gerar código assembly da linha {indice_linha + 1}: {gerar_codigo_assembly}")
            
            # token_values = [token.valor for token in tokens]
            # print(f"Tokens na linha {numero_linha}: {token_values}")
            # print(f"Resultado da linha {numero_linha}: {resultado}")
            # print(f"Memória após linha {numero_linha}: {memoria}")
            # print(f"Histórico após linha {numero_linha}: {historico}")
            
            
if __name__ == "__main__":
    main()