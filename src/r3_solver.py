from itertools import product

from src.formula import Variable, Not, And, Or, Implies, Iff


def get_variables(formula):
    """
    Retorna o conjunto de variáveis proposicionais
    presentes em uma fórmula.
    """

    # Caso a fórmula seja apenas uma variável
    if isinstance(formula, Variable):
        return {formula.name}

    # Caso seja uma negação, procura dentro do operando
    if isinstance(formula, Not):
        return get_variables(formula.operand)

    # Para operadores binários, procura nos dois lados da fórmula
    if isinstance(formula, (And, Or, Implies, Iff)):
        return get_variables(formula.left) | get_variables(formula.right)

    return set()


def find_models(formula):
    """
    Testa todas as valorações possíveis e retorna
    apenas aquelas que tornam a fórmula verdadeira.
    """

    # Descobre quais variáveis existem na fórmula
    variables = sorted(get_variables(formula))

    # Lista que armazenará as valorações que satisfazem a fórmula
    models = []

    # Gera todas as combinações possíveis de False e True
    for values in product([False, True], repeat=len(variables)):

        # Associa cada variável ao seu respectivo valor
        valuation = dict(zip(variables, values))

        # Se a fórmula for verdadeira nessa valoração,
        # ela é considerada um modelo
        if formula.evaluate(valuation):
            models.append(valuation)

    return models

def classify(formula):
    """
    Classifica a fórmula como:
    - válida
    - contingente
    - insatisfatível
    """

    # Descobre quantas variáveis existem
    variables = get_variables(formula)

    # Procura todas as valorações que tornam a fórmula verdadeira
    models = find_models(formula)

    # Número total de valorações possíveis: 2^n
    total_valuations = 2 ** len(variables)

    # Nenhuma valoração torna a fórmula verdadeira
    if len(models) == 0:
        return "insatisfatível"

    # Todas as valorações tornam a fórmula verdadeira
    if len(models) == total_valuations:
        return "válida"

    # Algumas tornam verdadeira e outras falsa
    return "contingente"

def model_count(formula):
    """
    Retorna a quantidade de modelos que satisfazem a fórmula.
    """

    return len(find_models(formula))


def first_model(formula):
    """
    Retorna um exemplo de modelo que satisfaz a fórmula.

    Se a fórmula for insatisfatível, retorna None.
    """

    models = find_models(formula)

    if len(models) == 0:
        return None

    return models[0]