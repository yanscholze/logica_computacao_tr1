import pytest

from src.parser import (
    parse_formula,
    tokenize,
    ParserError,
)


def test_tokenizer():
    tokens = tokenize("(P -> Q) & ~R")

    assert tokens == [
        "(",
        "P",
        "->",
        "Q",
        ")",
        "&",
        "~",
        "R",
    ]


def test_parser_exemplo_enunciado():
    formula = parse_formula("(P -> Q) & ~R")

    assert str(formula) == "((P → Q) ∧ ¬R)"


def test_precedencia():
    formula = parse_formula("P | Q & R")

    assert str(formula) == "(P ∨ (Q ∧ R))"


def test_parenteses_alteram_precedencia():
    formula = parse_formula("(P | Q) & R")

    assert str(formula) == "((P ∨ Q) ∧ R)"


def test_bicondicional():
    formula = parse_formula("P <-> Q")

    assert str(formula) == "(P ↔ Q)"


def test_negacoes_consecutivas():
    formula = parse_formula("~~P")

    assert str(formula) == "¬¬P"


def test_parser_avalia_formula():
    formula = parse_formula("(P -> Q) & ~R")

    valores = {
        "P": True,
        "Q": True,
        "R": False,
    }

    assert formula.evaluate(valores) is True


def test_formula_invalida():
    with pytest.raises(ParserError):
        parse_formula("(P & Q")