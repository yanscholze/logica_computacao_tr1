from src.formula import (
    Variable,
    Not,
    And,
    Or,
    Implies,
    Iff,
)

from src.tseitin import (
    tseitin,
    to_dimacs,
    formula_to_dimacs,
)

from src.dpll import dpll


def test_tseitin_variavel_simples():
    P = Variable("P")

    clauses, originals = tseitin(P)

    assert clauses == [["P"]]
    assert originals == {"P"}


def test_tseitin_conjuncao():
    P = Variable("P")
    Q = Variable("Q")

    formula = And(P, Q)

    clauses, originals = tseitin(formula)

    assert "P" in originals
    assert "Q" in originals

    # 3 cláusulas da equivalência
    # + 1 cláusula exigindo a raiz verdadeira.
    assert len(clauses) == 4


def test_tseitin_preserva_sat():
    P = Variable("P")
    Q = Variable("Q")

    formula = And(
        Or(P, Q),
        Not(P)
    )

    clauses, _ = tseitin(formula)

    satisfativel, modelo, _ = dpll(clauses)

    assert satisfativel is True
    assert modelo is not None


def test_tseitin_preserva_unsat():
    P = Variable("P")

    formula = And(
        P,
        Not(P)
    )

    clauses, _ = tseitin(formula)

    satisfativel, modelo, _ = dpll(clauses)

    assert satisfativel is False
    assert modelo is None


def test_tseitin_implicacao():
    P = Variable("P")
    Q = Variable("Q")

    formula = Implies(P, Q)

    clauses, _ = tseitin(formula)

    satisfativel, _, _ = dpll(clauses)

    assert satisfativel is True


def test_tseitin_bicondicional():
    P = Variable("P")
    Q = Variable("Q")

    formula = Iff(P, Q)

    clauses, _ = tseitin(formula)

    satisfativel, _, _ = dpll(clauses)

    assert satisfativel is True


def test_dimacs():
    clauses = [
        ["P", "¬Q"],
        ["Q", "R"],
    ]

    dimacs, variable_map = to_dimacs(clauses)

    assert dimacs.startswith("p cnf 3 2")

    assert variable_map == {
        "P": 1,
        "Q": 2,
        "R": 3,
    }

    assert "1 -2 0" in dimacs
    assert "2 3 0" in dimacs


def test_formula_para_dimacs():
    P = Variable("P")
    Q = Variable("Q")

    formula = And(P, Q)

    resultado = formula_to_dimacs(formula)

    assert "dimacs" in resultado
    assert "variable_map" in resultado
    assert "clauses" in resultado

    assert resultado["dimacs"].startswith("p cnf")




# TESTE DO SOLVER REAL

from src.solver_real import resolver_com_pysat


def test_pysat_formula_satisfativel():
    P = Variable("P")
    Q = Variable("Q")

    formula = And(P, Q)

    resultado = resolver_com_pysat(formula)

    assert resultado["satisfativel"] is True

    assert resultado["modelo"]["P"] is True
    assert resultado["modelo"]["Q"] is True


def test_pysat_formula_insatisfativel():
    P = Variable("P")

    formula = And(
        P,
        Not(P)
    )

    resultado = resolver_com_pysat(formula)

    assert resultado["satisfativel"] is False
    assert resultado["modelo"] is None