import unittest
from lexer_to_assembly import parseExpressao
from dfa import LexicalError


def token_values(tokens):
    return [token.valor for token in tokens]


class TestDFANumeros(unittest.TestCase):
    """Testes para reconhecimento de números"""
    
    def test_numero_inteiro(self):
        """Testa reconhecimento de número inteiro"""
        tokens = parseExpressao("42")
        self.assertEqual(token_values(tokens), ["42"])
    
    def test_numero_decimal(self):
        """Testa reconhecimento de número decimal"""
        tokens = parseExpressao("3.14")
        self.assertEqual(token_values(tokens), ["3.14"])
    
    def test_numero_negativo(self):
        """Testa reconhecimento de número negativo"""
        tokens = parseExpressao("-5")
        self.assertEqual(token_values(tokens), ["-5"])
    
    def test_numero_decimal_negativo(self):
        """Testa reconhecimento de número decimal negativo"""
        tokens = parseExpressao("-2.5")
        self.assertEqual(token_values(tokens), ["-2.5"])
    
    def test_numero_com_espaço(self):
        """Testa número seguido de espaço"""
        tokens = parseExpressao("10 ")
        self.assertEqual(token_values(tokens), ["10"])
    
    def test_multiplos_numeros(self):
        """Testa múltiplos números separados por espaço"""
        tokens = parseExpressao("1 2 3")
        self.assertEqual(token_values(tokens), ["1", "2", "3"])


class TestDFAOperadores(unittest.TestCase):
    """Testes para reconhecimento de operadores"""
    
    def test_operador_plus(self):
        """Testa reconhecimento de +"""
        tokens = parseExpressao("+")
        self.assertEqual(token_values(tokens), ["+"])
    
    def test_operador_minus(self):
        """Testa reconhecimento de - como operador"""
        with self.assertRaises(LexicalError):
            parseExpressao("1 -")
    
    def test_operador_multiplicacao(self):
        """Testa reconhecimento de *"""
        tokens = parseExpressao("*")
        self.assertEqual(token_values(tokens), ["*"])
    
    def test_operador_divisao(self):
        """Testa reconhecimento de /"""
        tokens = parseExpressao("/")
        self.assertEqual(token_values(tokens), ["/"])
    
    def test_operador_divisao_inteira(self):
        """Testa reconhecimento de //"""
        tokens = parseExpressao("//")
        self.assertEqual(token_values(tokens), ["//"])
    
    def test_operador_modulo(self):
        """Testa reconhecimento de %"""
        tokens = parseExpressao("%")
        self.assertEqual(token_values(tokens), ["%"])
    
    def test_operador_potencia(self):
        """Testa reconhecimento de ^ (potência)"""
        tokens = parseExpressao("^")
        self.assertEqual(token_values(tokens), ["^"])
    
    def test_multiplos_operadores(self):
        """Testa múltiplos operadores"""
        with self.assertRaises(LexicalError):
            parseExpressao("+ - *")


class TestDFAParenteses(unittest.TestCase):
    """Testes para reconhecimento de parênteses"""
    
    def test_parentese_aberta(self):
        """Testa reconhecimento de ("""
        tokens = parseExpressao("(")
        self.assertEqual(token_values(tokens), ["("])
    
    def test_parentese_fechada(self):
        """Testa reconhecimento de )"""
        tokens = parseExpressao(")")
        self.assertEqual(token_values(tokens), [")"])
    
    def test_parenteses_balanceados(self):
        """Testa parênteses balanceados"""
        tokens = parseExpressao("( )")
        self.assertEqual(token_values(tokens), ["(", ")"])
    
    def test_parenteses_desbalanceados(self):
        """Testa parênteses desbalanceados (sem erro, pois removemos validação)"""
        tokens = parseExpressao(") )")
        self.assertEqual(token_values(tokens), [")", ")"])


class TestDFAPalavras(unittest.TestCase):
    """Testes para reconhecimento de palavras (RES, MEM)"""
    
    def test_palavra_RES(self):
        """Testa reconhecimento de RES"""
        tokens = parseExpressao("RES")
        self.assertEqual(token_values(tokens), ["RES"])
    
    def test_palavra_MEM(self):
        """Testa reconhecimento de MEM"""
        tokens = parseExpressao("MEM")
        self.assertEqual(token_values(tokens), ["MEM"])
    
    def test_palavras_multiplas(self):
        """Testa múltiplas palavras"""
        tokens = parseExpressao("RES MEM")
        self.assertEqual(token_values(tokens), ["RES", "MEM"])
    
    def test_palavra_customizada(self):
        """Testa palavra customizada (letras maiúsculas)"""
        tokens = parseExpressao("CUSTOM")
        self.assertEqual(token_values(tokens), ["CUSTOM"])


class TestDFAExpressoesCompletas(unittest.TestCase):
    """Testes para expressões completas em notação RPN"""
    
    def test_expressao_simples(self):
        """Testa expressão: 1 2 +"""
        tokens = parseExpressao("1 2 +")
        self.assertEqual(token_values(tokens), ["1", "2", "+"])
    
    def test_expressao_com_decimais(self):
        """Testa expressão: 3.14 2.71 *"""
        tokens = parseExpressao("3.14 2.71 *")
        self.assertEqual(token_values(tokens), ["3.14", "2.71", "*"])
    
    def test_expressao_com_parenteses(self):
        """Testa expressão: ( 1 2 + )"""
        tokens = parseExpressao("( 1 2 + )")
        self.assertEqual(token_values(tokens), ["(", "1", "2", "+", ")"])
    
    def test_expressao_complexa(self):
        """Testa expressão complexa: ( 3.14 -2 * ) 5 /"""
        tokens = parseExpressao("( 3.14 -2 * ) 5 /")
        self.assertEqual(token_values(tokens), ["(", "3.14", "-2", "*", ")", "5", "/"])
    
    def test_expressao_com_divisao_inteira(self):
        """Testa expressão com //: 10 3 //"""
        tokens = parseExpressao("10 3 //")
        self.assertEqual(token_values(tokens), ["10", "3", "//"])
    
    def test_expressao_com_modulo(self):
        """Testa expressão com %: 10 3 %"""
        tokens = parseExpressao("10 3 %")
        self.assertEqual(token_values(tokens), ["10", "3", "%"])
    
    def test_expressao_com_potencia(self):
        """Testa expressão com ^: 2 3 ^"""
        tokens = parseExpressao("2 3 ^")
        self.assertEqual(token_values(tokens), ["2", "3", "^"])


class TestDFAErrosLexicos(unittest.TestCase):
    """Testes para detecção de erros léxicos"""
    
    def test_numero_decimal_malformado_multiplos_pontos(self):
        """Testa número com múltiplos pontos: 3.14.5"""
        with self.assertRaises(LexicalError):
            parseExpressao("3.14.5")
    
    def test_numero_decimal_sem_digitos_apos_ponto(self):
        """Testa número com ponto sem dígitos: 3."""
        with self.assertRaises(LexicalError):
            parseExpressao("3.")
    
    def test_numero_negativo_sem_digito(self):
        """Testa número negativo malformado: - (é tratado como operador)"""
        with self.assertRaises(LexicalError):
            parseExpressao("-")
    
    def test_numero_negativo_seguido_de_nao_digito(self):
        """Testa - seguido de não número no contexto de número negativo"""
        with self.assertRaises(LexicalError):
            parseExpressao("-.5")
    
    def test_caractere_invalido_minuscula(self):
        """Testa caractere inválido (letra minúscula)"""
        with self.assertRaises(LexicalError):
            parseExpressao("abc")
    
    def test_caractere_invalido_especial(self):
        """Testa caractere especial inválido: &"""
        with self.assertRaises(LexicalError):
            parseExpressao("&")
    
    def test_operador_seguido_de_operador(self):
        """Testa operador seguido de operador (válido na nova regra)"""
        tokens = parseExpressao("+*")
        self.assertEqual(token_values(tokens), ["+", "*"])
    
    def test_palavra_seguida_de_letra_minuscula(self):
        """Testa palavra seguida de letra minúscula"""
        with self.assertRaises(LexicalError):
            parseExpressao("RESa")


class TestDFADelimitadores(unittest.TestCase):
    """Testes para validação de delimitadores"""
    
    def test_numero_seguido_de_parentese(self):
        """Testa número seguido de parêntese (delimitador válido)"""
        tokens = parseExpressao("5(")
        self.assertEqual(token_values(tokens), ["5", "("])
    
    def test_palavra_seguida_de_parentese(self):
        """Testa palavra seguida de parêntese"""
        tokens = parseExpressao("RES(")
        self.assertEqual(token_values(tokens), ["RES", "("])
    
    def test_numero_seguido_de_operador(self):
        """Testa número seguido de operador (delimitador válido na nova regra)"""
        tokens = parseExpressao("5+")
        self.assertEqual(token_values(tokens), ["5", "+"])


class TestDFACasosPraticos(unittest.TestCase):
    """Testes com casos práticos de uso"""
    
    def test_calculo_basico_rpn(self):
        """Testa: (3 4 +) 2 * -- resultado deveria ser 14"""
        tokens = parseExpressao("( 3 4 + ) 2 *")
        self.assertEqual(token_values(tokens), ["(", "3", "4", "+", ")", "2", "*"])
    
    def test_expressao_com_resgate_memoria(self):
        """Testa expressão com RES e MEM"""
        tokens = parseExpressao("RES 5 MEM")
        self.assertEqual(token_values(tokens), ["RES", "5", "MEM"])
    
    def test_expressao_vazia(self):
        """Testa linha vazia"""
        tokens = parseExpressao("")
        self.assertEqual(tokens, [])
    
    def test_expressao_apenas_espacos(self):
        """Testa linha com apenas espaços"""
        tokens = parseExpressao("   ")
        self.assertEqual(tokens, [])


if __name__ == "__main__":
    unittest.main()
