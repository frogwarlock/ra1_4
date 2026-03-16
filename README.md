# Analisador Léxico e Gerador de Assembly para ARMv7 

# Funcionamento

## Executar o Analisador Léxico

```bash
python3 lexer_to_assembly.py <arquivo>.txt
```

Exemplo:
```bash
python3 lexer_to_assembly.py teste.txt
```

Saída esperada:
```
Tokens na linha 1: ['(', '1', '2', '+', ')']
Tokens na linha 2: ['3.14', '2.71', '*']
```

## Testes Unitários

- Reconhecimento de números (inteiros, decimais, negativos)
- Validação de operadores (+, -, *, /, //, %, ^)
- Reconhecimento de parênteses
- Palavras especiais (RES, MEM)
- Expressões completas em notação RPN
- Detecção de erros léxicos
- Validação de delimitadores

### Executar todos os testes

```bash
python3 -m unittest test_dfa -v
```

### Executar testes de uma categoria específica

```bash
# Apenas testes de números
python3 -m unittest test_dfa.TestDFANumeros -v

# Apenas testes de operadores
python3 -m unittest test_dfa.TestDFAOperadores -v

# Apenas testes de erros léxicos
python3 -m unittest test_dfa.TestDFAErrosLexicos -v
```

### Executar um teste específico

```bash
python3 -m unittest test_dfa.TestDFANumeros.test_numero_decimal -v
```



# Informações adicionais
Pontíficia Universidade Católica do Paraná - PUCPR

Construção de Interpretadores, 7º Período ministrada pelo professor Frank Coelho de Alcantara

Trabalho desenvolvido por Isabella Lucena Conceição