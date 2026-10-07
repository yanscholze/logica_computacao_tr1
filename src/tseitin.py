from src.formula import (
    Variable,
    Not,
    And,
    Or,
    Implies,
    Iff,
)


class TseitinEncoder:
    """
    Converte uma AST proposicional para FNC utilizando
    a transformação de Tseitin.

    Cada subfórmula recebe uma variável auxiliar.

    A transformação preserva satisfatibilidade e produz
    uma FNC de tamanho linear em relação à AST.
    """

    def __init__(self):
        self.clauses = []
        self.counter = 0
        self.variable_ids = {}
        self.original_variables = set()

    def new_auxiliary(self):
        """
        Cria uma nova variável auxiliar.
        """

        self.counter += 1
        return f"_t{self.counter}"

    def encode(self, formula):
        """
        Codifica recursivamente uma fórmula.

        Retorna o nome da variável que representa
        o resultado da subfórmula.
        """

        # ----------------------------------------------------
        # Variável proposicional
        # ----------------------------------------------------

        if isinstance(formula, Variable):
            self.original_variables.add(formula.name)
            return formula.name

        # ----------------------------------------------------
        # Negação
        #
        # t ↔ ¬a
        #
        # (¬t ∨ ¬a) ∧ (t ∨ a)
        # ----------------------------------------------------

        if isinstance(formula, Not):
            a = self.encode(formula.operand)
            t = self.new_auxiliary()

            self.clauses.append([f"¬{t}", f"¬{a}"])
            self.clauses.append([t, a])

            return t

        # ----------------------------------------------------
        # Conjunção
        #
        # t ↔ (a ∧ b)
        #
        # (¬t ∨ a)
        # (¬t ∨ b)
        # (t ∨ ¬a ∨ ¬b)
        # ----------------------------------------------------

        if isinstance(formula, And):
            a = self.encode(formula.left)
            b = self.encode(formula.right)
            t = self.new_auxiliary()

            self.clauses.append([f"¬{t}", a])
            self.clauses.append([f"¬{t}", b])
            self.clauses.append([t, f"¬{a}", f"¬{b}"])

            return t

        # ----------------------------------------------------
        # Disjunção
        #
        # t ↔ (a ∨ b)
        #
        # (t ∨ ¬a)
        # (t ∨ ¬b)
        # (¬t ∨ a ∨ b)
        # ----------------------------------------------------

        if isinstance(formula, Or):
            a = self.encode(formula.left)
            b = self.encode(formula.right)
            t = self.new_auxiliary()

            self.clauses.append([t, f"¬{a}"])
            self.clauses.append([t, f"¬{b}"])
            self.clauses.append([f"¬{t}", a, b])

            return t

        # ----------------------------------------------------
        # Implicação
        #
        # a → b equivale a ¬a ∨ b.
        #
        # t ↔ (¬a ∨ b)
        # ----------------------------------------------------

        if isinstance(formula, Implies):
            a = self.encode(formula.left)
            b = self.encode(formula.right)
            t = self.new_auxiliary()

            self.clauses.append([t, a])
            self.clauses.append([t, f"¬{b}"])
            self.clauses.append([f"¬{t}", f"¬{a}", b])

            return t

        # ----------------------------------------------------
        # Bicondicional
        #
        # t ↔ (a ↔ b)
        # ----------------------------------------------------

        if isinstance(formula, Iff):
            a = self.encode(formula.left)
            b = self.encode(formula.right)
            t = self.new_auxiliary()

            self.clauses.append([f"¬{t}", f"¬{a}", b])
            self.clauses.append([f"¬{t}", a, f"¬{b}"])
            self.clauses.append([t, a, b])
            self.clauses.append([t, f"¬{a}", f"¬{b}"])

            return t

        raise TypeError(
            f"Tipo de fórmula não suportado: {type(formula)}"
        )

    def transform(self, formula):
        """
        Executa a transformação completa.

        Além das cláusulas geradas para as subfórmulas,
        adiciona uma cláusula unitária exigindo que a
        variável que representa a fórmula inteira seja
        verdadeira.
        """

        root = self.encode(formula)

        # A fórmula original deve ser verdadeira.
        self.clauses.append([root])

        return self.clauses


def tseitin(formula):
    """
    Interface simples para executar a transformação.

    Retorna:
        cláusulas,
        variáveis originais
    """

    encoder = TseitinEncoder()

    clauses = encoder.transform(formula)

    return clauses, encoder.original_variables


# ============================================================
# DIMACS
# ============================================================

def literal_name(literal):
    """
    Remove a negação de um literal.

    Exemplo:
        ¬P -> P
        P  -> P
    """

    if literal.startswith("¬"):
        return literal[1:]

    return literal


def to_dimacs(clauses):
    """
    Converte uma lista de cláusulas para o formato DIMACS CNF.

    Retorna:
        texto DIMACS,
        mapa variável -> número
    """

    variables = set()

    for clause in clauses:
        for literal in clause:
            variables.add(literal_name(literal))

    variables = sorted(variables)

    variable_map = {
        variable: index
        for index, variable in enumerate(
            variables,
            start=1
        )
    }

    lines = []

    # Cabeçalho DIMACS:
    #
    # p cnf <quantidade_variaveis> <quantidade_clausulas>
    lines.append(
        f"p cnf {len(variable_map)} {len(clauses)}"
    )

    for clause in clauses:
        numbers = []

        for literal in clause:
            variable = literal_name(literal)
            number = variable_map[variable]

            if literal.startswith("¬"):
                number = -number

            numbers.append(str(number))

        # Toda cláusula DIMACS termina em 0.
        lines.append(
            " ".join(numbers) + " 0"
        )

    return "\n".join(lines), variable_map


def formula_to_dimacs(formula):
    """
    Converte diretamente uma fórmula da AST para DIMACS
    utilizando Tseitin.
    """

    clauses, original_variables = tseitin(formula)

    dimacs, variable_map = to_dimacs(clauses)

    return {
        "clauses": clauses,
        "original_variables": original_variables,
        "variable_map": variable_map,
        "dimacs": dimacs,
    }