from pysat.solvers import Solver

from src.tseitin import (
    tseitin,
    literal_name,
)


def resolver_com_pysat(formula):
    """
    Resolve uma fórmula utilizando um SAT solver real
    da biblioteca PySAT.

    A fórmula é primeiro convertida para FNC por Tseitin.
    """

    clauses, original_variables = tseitin(formula)

    # Descobre todas as variáveis, incluindo as auxiliares.
    variables = sorted({
        literal_name(literal)
        for clause in clauses
        for literal in clause
    })

    variable_map = {
        variable: index
        for index, variable in enumerate(
            variables,
            start=1
        )
    }

    numeric_clauses = []

    for clause in clauses:
        numeric_clause = []

        for literal in clause:
            variable = literal_name(literal)

            number = variable_map[variable]

            if literal.startswith("¬"):
                number = -number

            numeric_clause.append(number)

        numeric_clauses.append(numeric_clause)

    with Solver() as solver:

        for clause in numeric_clauses:
            solver.add_clause(clause)

        satisfativel = solver.solve()

        if not satisfativel:
            return {
                "satisfativel": False,
                "modelo": None,
            }

        numeric_model = solver.get_model()

    numeric_model = set(numeric_model)

    modelo = {}

    # Retornamos somente as variáveis da fórmula original,
    # escondendo as auxiliares criadas por Tseitin.
    for variable in sorted(original_variables):
        number = variable_map[variable]

        modelo[variable] = number in numeric_model

    return {
        "satisfativel": True,
        "modelo": modelo,
    }