from itertools import product

from src.formula import Variable, Not, And, Or, Implies
from src.r3_solver import get_variables
from src.r4_cnf import (
    eliminate_implications,
    to_nnf,
    distribute_or_over_and,
    to_cnf,
    cnf_to_clauses,
)


def formulas_equivalentes(formula1, formula2):
    """
    Compara duas fórmulas em todas as valorações possíveis.
    """

    # Descobre todas as variáveis presentes nas duas fórmulas
    variaveis = sorted(
        get_variables(formula1) | get_variables(formula2)
    )

    # Testa todas as combinações possíveis de True e False
    for valores in product(
        [False, True],
        repeat=len(variaveis)
    ):
        valoracao = dict(zip(variaveis, valores))

        # Se algum resultado for diferente,
        # as fórmulas não são equivalentes
        if (
            formula1.evaluate(valoracao)
            != formula2.evaluate(valoracao)
        ):
            return False

    return True


def test_eliminar_implicacao():
    """
    Verifica:
    P → Q equivale a ¬P ∨ Q.
    """

    P = Variable("P")
    Q = Variable("Q")

    formula = Implies(P, Q)

    resultado = eliminate_implications(formula)

    assert str(resultado) == "(¬P ∨ Q)"


def test_dupla_negacao():
    """
    Verifica:
    ¬¬P equivale a P.
    """

    P = Variable("P")

    formula = Not(Not(P))

    resultado = to_nnf(formula)

    assert str(resultado) == "P"


def test_de_morgan():
    """
    Verifica:
    ¬(P ∧ Q) equivale a ¬P ∨ ¬Q.
    """

    P = Variable("P")
    Q = Variable("Q")

    formula = Not(And(P, Q))

    resultado = to_nnf(formula)

    assert str(resultado) == "(¬P ∨ ¬Q)"


def test_distribuicao():
    """
    Verifica a distribuição de OR sobre AND.
    """

    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    formula = Or(
        P,
        And(Q, R)
    )

    resultado = distribute_or_over_and(formula)

    assert str(resultado) == "((P ∨ Q) ∧ (P ∨ R))"


def test_lista_de_clausulas():
    """
    Verifica a conversão da FNC
    para uma lista de cláusulas.
    """

    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    formula = And(
        Or(P, Q),
        Or(Not(P), R)
    )

    clausulas = cnf_to_clauses(formula)

    assert clausulas == [
        ["P", "Q"],
        ["¬P", "R"]
    ]


def test_fnc_equivalente_formula_original():
    """
    Compara a fórmula original e sua FNC
    em todas as valorações possíveis.
    """

    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    formula_original = Implies(
        P,
        And(Q, R)
    )

    fnc = to_cnf(formula_original)

    assert formulas_equivalentes(
        formula_original,
        fnc
    )