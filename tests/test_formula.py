from src.formula import Variable, And, Implies


def test_implicacao_falsa():
    B = Variable("B")
    E = Variable("E")
    M = Variable("M")

    formula = Implies(
        And(B, E),
        M
    )

    valores = {
        "B": True,
        "E": True,
        "M": False
    }

    assert formula.evaluate(valores) == False