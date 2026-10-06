from src.diagnostico import (
    analisar_estado,
    regras_violadas,
    SISTEMA,
    SISTEMA_INSATISFATIVEL
)

from src.r3_solver import (
    classify,
    model_count
)


def test_estado_consistente():
    valores = {
        "B": True,
        "M": True,
        "C": True,
        "I": True,
        "E": True,
        "P": True
    }

    resultado = analisar_estado(valores)

    assert resultado["consistente"] is True
    assert resultado["violadas"] == []


def test_estado_inconsistente():
    valores = {
        "B": True,
        "M": False,
        "C": True,
        "I": True,
        "E": True,
        "P": False
    }

    resultado = analisar_estado(valores)

    assert resultado["consistente"] is False
    assert len(resultado["violadas"]) > 0


def test_sistema_possui_modelos():
    assert model_count(SISTEMA) > 0


def test_variante_insatisfativel():
    assert classify(SISTEMA_INSATISFATIVEL) == "insatisfatível"
    assert model_count(SISTEMA_INSATISFATIVEL) == 0