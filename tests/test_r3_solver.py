from src.formula import Variable, Or, And, Not
from src.r3_solver import (
    find_models,
    classify,
    model_count,
    first_model,
)


def test_formula_valida():
    """
    Testa uma fórmula válida (tautologia).

    A fórmula P ∨ ¬P é sempre verdadeira,
    independentemente do valor de P.
    """

    P = Variable("P")

    formula = Or(P, Not(P))

    modelos = find_models(formula)

    assert len(modelos) == 2
    assert classify(formula) == "válida"


def test_formula_insatisfativel():
    """
    Testa uma fórmula insatisfatível (contradição).

    A fórmula P ∧ ¬P nunca pode ser verdadeira.
    """

    P = Variable("P")

    formula = And(P, Not(P))

    modelos = find_models(formula)

    assert len(modelos) == 0
    assert classify(formula) == "insatisfatível"


def test_formula_contingente():
    """
    Testa uma fórmula contingente.

    A fórmula P ∧ Q é verdadeira em algumas valorações
    e falsa em outras.
    """

    P = Variable("P")
    Q = Variable("Q")

    formula = And(P, Q)

    modelos = find_models(formula)

    assert len(modelos) == 1
    assert classify(formula) == "contingente"


def test_contagem_de_modelos():
    """
    Testa a contagem de modelos de uma fórmula.
    """

    P = Variable("P")
    Q = Variable("Q")

    formula = And(P, Q)

    assert model_count(formula) == 1


def test_primeiro_modelo():
    """
    Testa se o programa consegue retornar
    um exemplo de modelo que satisfaz a fórmula.
    """

    P = Variable("P")

    formula = P

    modelo = first_model(formula)

    assert modelo == {"P": True}