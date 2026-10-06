from itertools import product

from src.formula import (
    Variable,
    Not,
    And,
    Or,
    Implies,
    Iff
)

from src.r3_solver import classify
from src.r4_cnf import to_cnf


def formulas_equivalentes(formula1, formula2):
    """
    Compara duas fórmulas em todas as valorações possíveis.

    As fórmulas são equivalentes quando apresentam o mesmo
    resultado para todas as linhas da tabela-verdade.
    """

    variaveis = sorted(
        formula1.variables() | formula2.variables()
    )

    for valores in product(
        [False, True],
        repeat=len(variaveis)
    ):
        valoracao = dict(zip(variaveis, valores))

        resultado1 = formula1.evaluate(valoracao)
        resultado2 = formula2.evaluate(valoracao)

        if resultado1 != resultado2:
            return False

    return True


def test_tautologia():
    P = Variable("P")

    formula = Or(P, Not(P))

    assert classify(formula) == "válida"


def test_contradicao():
    P = Variable("P")

    formula = And(P, Not(P))

    assert classify(formula) == "insatisfatível"


def test_formula_contingente():
    P = Variable("P")
    Q = Variable("Q")

    formula = Implies(P, Q)

    assert classify(formula) == "contingente"


def test_bicondicional_contingente():
    P = Variable("P")
    Q = Variable("Q")

    formula = Iff(P, Q)

    assert classify(formula) == "contingente"


def test_fnc_equivalente():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    formula_original = And(
        Implies(P, Q),
        Implies(Q, R)
    )

    formula_fnc = to_cnf(formula_original)

    assert formulas_equivalentes(
        formula_original,
        formula_fnc
    )


def test_fnc_equivalente_com_bicondicional():
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")

    formula_original = Iff(
        P,
        Or(Q, R)
    )

    formula_fnc = to_cnf(formula_original)

    assert formulas_equivalentes(
        formula_original,
        formula_fnc
    )