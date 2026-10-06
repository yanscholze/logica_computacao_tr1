from src.formula import (
    Variable,
    Not,
    And,
    Or,
)

from src.dpll import (
    dpll,
    resolver_dpll,
)

from src.r4_cnf import to_cnf


def test_dpll_formula_satisfativel():
    clausulas = [
        ["P", "Q"],
        ["¬P", "Q"],
    ]

    satisfativel, modelo, rastro = dpll(clausulas)

    assert satisfativel is True
    assert modelo is not None
    assert len(rastro) > 0


def test_dpll_formula_insatisfativel():
    clausulas = [
        ["P"],
        ["¬P"],
    ]

    satisfativel, modelo, rastro = dpll(clausulas)

    assert satisfativel is False
    assert modelo is None


def test_propagacao_unitaria():
    clausulas = [
        ["P"],
        ["¬P", "Q"],
    ]

    satisfativel, modelo, rastro = dpll(clausulas)

    assert satisfativel is True

    assert modelo["P"] is True
    assert modelo["Q"] is True

    assert any(
        "Propagação unitária" in passo
        for passo in rastro
    )


def test_dpll_com_ast():
    P = Variable("P")
    Q = Variable("Q")

    formula = And(
        Or(P, Q),
        Not(P)
    )

    satisfativel, modelo, rastro = resolver_dpll(
        formula,
        to_cnf
    )

    assert satisfativel is True
    assert modelo["P"] is False
    assert modelo["Q"] is True


def test_dpll_ast_insatisfativel():
    P = Variable("P")

    formula = And(
        P,
        Not(P)
    )

    satisfativel, modelo, rastro = resolver_dpll(
        formula,
        to_cnf
    )

    assert satisfativel is False
    assert modelo is None