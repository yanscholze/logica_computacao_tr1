from src.formula import Not


def literal_info(literal):
    """
    Converte um literal da AST para:
        (nome_da_variavel, valor_necessario)

    Exemplos:
        P  -> ("P", True)
        ¬P -> ("P", False)
    """

    if isinstance(literal, Not):
        return literal.operand.name, False

    return literal.name, True


def simplificar_clausulas(clausulas, variavel, valor):
    """
    Simplifica a lista de cláusulas após atribuir um valor
    a uma variável.

    Uma cláusula satisfeita é removida.

    O literal que se torna falso é removido das cláusulas
    restantes.
    """

    literal_verdadeiro = variavel if valor else f"¬{variavel}"
    literal_falso = f"¬{variavel}" if valor else variavel

    novas_clausulas = []

    for clausula in clausulas:

        # A cláusula já foi satisfeita.
        if literal_verdadeiro in clausula:
            continue

        # Remove o literal que agora sabemos ser falso.
        nova_clausula = [
            literal
            for literal in clausula
            if literal != literal_falso
        ]

        novas_clausulas.append(nova_clausula)

    return novas_clausulas


def interpretar_literal(literal):
    """
    Interpreta um literal textual.

    Exemplos:
        "P"  -> ("P", True)
        "¬P" -> ("P", False)
    """

    if literal.startswith("¬"):
        return literal[1:], False

    return literal, True


def encontrar_clausula_unitaria(clausulas):
    """
    Procura uma cláusula que contenha exatamente um literal.
    """

    for clausula in clausulas:
        if len(clausula) == 1:
            return clausula[0]

    return None


def escolher_literal(clausulas):
    """
    Escolhe um literal para iniciar uma ramificação.

    Esta implementação utiliza o primeiro literal disponível.
    """

    for clausula in clausulas:
        if clausula:
            return clausula[0]

    return None


def dpll(clausulas, atribuicoes=None, rastro=None, nivel=0):
    """
    Resolve uma fórmula em FNC utilizando o algoritmo DPLL.

    Retorna:
        satisfativel
        atribuicoes encontradas
        rastro da execução
    """

    if atribuicoes is None:
        atribuicoes = {}

    if rastro is None:
        rastro = []

    # Criamos cópias para não alterar os dados recebidos.
    clausulas = [
        list(clausula)
        for clausula in clausulas
    ]

    atribuicoes = dict(atribuicoes)

    # --------------------------------------------------------
    # Propagação unitária
    # --------------------------------------------------------

    while True:
        literal = encontrar_clausula_unitaria(clausulas)

        if literal is None:
            break

        variavel, valor = interpretar_literal(literal)

        # Detecta atribuições contraditórias.
        if (
            variavel in atribuicoes
            and atribuicoes[variavel] != valor
        ):
            rastro.append(
                f"{'  ' * nivel}Conflito: "
                f"{variavel} recebeu valores incompatíveis."
            )

            return False, None, rastro

        atribuicoes[variavel] = valor

        rastro.append(
            f"{'  ' * nivel}"
            f"Propagação unitária: "
            f"{variavel} = {valor}"
        )

        clausulas = simplificar_clausulas(
            clausulas,
            variavel,
            valor
        )

        # Uma cláusula vazia representa contradição.
        if [] in clausulas:
            rastro.append(
                f"{'  ' * nivel}"
                "Conflito: cláusula vazia encontrada."
            )

            return False, None, rastro

        # Nenhuma cláusula restante:
        # todas foram satisfeitas.
        if not clausulas:
            rastro.append(
                f"{'  ' * nivel}"
                "SAT: todas as cláusulas foram satisfeitas."
            )

            return True, atribuicoes, rastro

    # --------------------------------------------------------
    # Casos-base
    # --------------------------------------------------------

    if not clausulas:
        rastro.append(
            f"{'  ' * nivel}"
            "SAT: todas as cláusulas foram satisfeitas."
        )

        return True, atribuicoes, rastro

    if [] in clausulas:
        rastro.append(
            f"{'  ' * nivel}"
            "UNSAT: cláusula vazia encontrada."
        )

        return False, None, rastro

    # --------------------------------------------------------
    # Escolha de variável / branching
    # --------------------------------------------------------

    literal = escolher_literal(clausulas)

    variavel, valor_original = interpretar_literal(literal)

    # Primeiro tentamos o valor sugerido pelo literal escolhido.
    for valor in [valor_original, not valor_original]:

        rastro.append(
            f"{'  ' * nivel}"
            f"Tentativa: {variavel} = {valor}"
        )

        novas_atribuicoes = dict(atribuicoes)
        novas_atribuicoes[variavel] = valor

        novas_clausulas = simplificar_clausulas(
            clausulas,
            variavel,
            valor
        )

        satisfativel, modelo, rastro = dpll(
            novas_clausulas,
            novas_atribuicoes,
            rastro,
            nivel + 1
        )

        if satisfativel:
            return True, modelo, rastro

        rastro.append(
            f"{'  ' * nivel}"
            f"Backtracking: desfazendo "
            f"{variavel} = {valor}"
        )

    return False, None, rastro


def resolver_dpll(formula, conversor_cnf):
    """
    Recebe uma fórmula da AST do projeto, converte para FNC
    e executa o DPLL.

    O conversor é recebido como parâmetro para manter
    este módulo independente da implementação da FNC.
    """

    formula_cnf = conversor_cnf(formula)

    # Import local para evitar dependência desnecessária
    # durante a inicialização do módulo.
    from src.r4_cnf import cnf_to_clauses

    clausulas = cnf_to_clauses(formula_cnf)

    return dpll(clausulas)