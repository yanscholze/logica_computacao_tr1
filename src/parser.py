from src.formula import (
    Variable,
    Not,
    And,
    Or,
    Implies,
    Iff,
)


class ParserError(Exception):
    """Erro encontrado durante a leitura de uma fórmula."""
    pass


# ============================================================
# Tokenização
# ============================================================

def tokenize(text):
    """
    Transforma o texto da fórmula em uma lista de tokens.

    Exemplo:
        "(P -> Q) & ~R"

    torna-se:
        ["(", "P", "->", "Q", ")", "&", "~", "R"]
    """

    tokens = []
    i = 0

    while i < len(text):
        char = text[i]

        # Ignora espaços
        if char.isspace():
            i += 1
            continue

        # Operadores com dois caracteres
        if text.startswith("<->", i):
            tokens.append("<->")
            i += 3
            continue

        if text.startswith("->", i):
            tokens.append("->")
            i += 2
            continue

        # Operadores e parênteses com um caractere
        if char in "()&|~":
            tokens.append(char)
            i += 1
            continue

        # Nome de variável
        if char.isalpha():
            inicio = i

            while i < len(text) and (
                text[i].isalnum() or text[i] == "_"
            ):
                i += 1

            tokens.append(text[inicio:i])
            continue

        raise ParserError(
            f"Caractere inválido na fórmula: {char}"
        )

    return tokens


# ============================================================
# Parser
# ============================================================

class Parser:
    """
    Parser recursivo para fórmulas proposicionais.

    Precedência, da maior para a menor:

        ~       negação
        &       conjunção
        |       disjunção
        ->      implicação
        <->     bicondicional
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        """Retorna o token atual."""

        if self.position >= len(self.tokens):
            return None

        return self.tokens[self.position]

    def consume(self, expected=None):
        """
        Consome o token atual.

        Se expected for informado, verifica se o token
        encontrado corresponde ao esperado.
        """

        token = self.current()

        if token is None:
            raise ParserError(
                "Fim inesperado da fórmula."
            )

        if expected is not None and token != expected:
            raise ParserError(
                f"Esperado '{expected}', encontrado '{token}'."
            )

        self.position += 1

        return token

    # --------------------------------------------------------
    # Bicondicional
    # --------------------------------------------------------

    def parse_iff(self):
        left = self.parse_implies()

        while self.current() == "<->":
            self.consume("<->")

            right = self.parse_implies()

            left = Iff(left, right)

        return left

    # --------------------------------------------------------
    # Implicação
    # --------------------------------------------------------

    def parse_implies(self):
        left = self.parse_or()

        if self.current() == "->":
            self.consume("->")

            # Chamada recursiva para permitir:
            # P -> Q -> R
            right = self.parse_implies()

            return Implies(left, right)

        return left

    # --------------------------------------------------------
    # Disjunção
    # --------------------------------------------------------

    def parse_or(self):
        left = self.parse_and()

        while self.current() == "|":
            self.consume("|")

            right = self.parse_and()

            left = Or(left, right)

        return left

    # --------------------------------------------------------
    # Conjunção
    # --------------------------------------------------------

    def parse_and(self):
        left = self.parse_not()

        while self.current() == "&":
            self.consume("&")

            right = self.parse_not()

            left = And(left, right)

        return left

    # --------------------------------------------------------
    # Negação
    # --------------------------------------------------------

    def parse_not(self):
        if self.current() == "~":
            self.consume("~")

            return Not(
                self.parse_not()
            )

        return self.parse_atom()

    # --------------------------------------------------------
    # Variáveis e parênteses
    # --------------------------------------------------------

    def parse_atom(self):
        token = self.current()

        if token is None:
            raise ParserError(
                "Era esperada uma variável ou expressão."
            )

        # Expressão entre parênteses
        if token == "(":
            self.consume("(")

            formula = self.parse_iff()

            self.consume(")")

            return formula

        # Variável
        if token[0].isalpha():
            self.consume()

            return Variable(token)

        raise ParserError(
            f"Token inesperado: '{token}'."
        )


# ============================================================
# Função pública
# ============================================================

def parse_formula(text):
    """
    Converte uma fórmula escrita em texto para a AST do projeto.

    Exemplo:
        parse_formula("(P -> Q) & ~R")
    """

    tokens = tokenize(text)

    if not tokens:
        raise ParserError(
            "A fórmula não pode ser vazia."
        )

    parser = Parser(tokens)

    formula = parser.parse_iff()

    # Depois do parser terminar, nenhum token pode sobrar.
    if parser.current() is not None:
        raise ParserError(
            f"Token inesperado: '{parser.current()}'."
        )

    return formula