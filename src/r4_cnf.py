from src.formula import Variable, Not, And, Or, Implies, Iff


def eliminate_implications(formula):
    """
    Elimina os conectivos de implicação (→) e bicondicional (↔).

    Equivalências utilizadas:
    A → B  ≡  ¬A ∨ B
    A ↔ B  ≡  (¬A ∨ B) ∧ (¬B ∨ A)
    """

    # Variáveis não precisam ser modificadas
    if isinstance(formula, Variable):
        return formula

    # Continua procurando dentro da negação
    if isinstance(formula, Not):
        return Not(eliminate_implications(formula.operand))

    # Continua procurando nos dois lados da conjunção
    if isinstance(formula, And):
        return And(
            eliminate_implications(formula.left),
            eliminate_implications(formula.right)
        )

    # Continua procurando nos dois lados da disjunção
    if isinstance(formula, Or):
        return Or(
            eliminate_implications(formula.left),
            eliminate_implications(formula.right)
        )

    # A → B equivale a ¬A ∨ B
    if isinstance(formula, Implies):
        left = eliminate_implications(formula.left)
        right = eliminate_implications(formula.right)

        return Or(Not(left), right)

    # A ↔ B equivale a:
    # (¬A ∨ B) ∧ (¬B ∨ A)
    if isinstance(formula, Iff):
        left = eliminate_implications(formula.left)
        right = eliminate_implications(formula.right)

        return And(
            Or(Not(left), right),
            Or(Not(right), left)
        )

    raise TypeError("Tipo de fórmula desconhecido.")


def to_nnf(formula):
    """
    Converte uma fórmula sem → e ↔ para a
    Forma Normal da Negação (FNN).

    Na FNN, as negações aparecem apenas
    diretamente sobre variáveis.
    """

    # Uma variável já está em FNN
    if isinstance(formula, Variable):
        return formula

    # Mantém conjunções e processa seus dois lados
    if isinstance(formula, And):
        return And(
            to_nnf(formula.left),
            to_nnf(formula.right)
        )

    # Mantém disjunções e processa seus dois lados
    if isinstance(formula, Or):
        return Or(
            to_nnf(formula.left),
            to_nnf(formula.right)
        )

    if isinstance(formula, Not):
        operand = formula.operand

        # Negação diretamente sobre uma variável
        if isinstance(operand, Variable):
            return formula

        # Dupla negação:
        # ¬¬A ≡ A
        if isinstance(operand, Not):
            return to_nnf(operand.operand)

        # Lei de De Morgan:
        # ¬(A ∧ B) ≡ ¬A ∨ ¬B
        if isinstance(operand, And):
            return Or(
                to_nnf(Not(operand.left)),
                to_nnf(Not(operand.right))
            )

        # Lei de De Morgan:
        # ¬(A ∨ B) ≡ ¬A ∧ ¬B
        if isinstance(operand, Or):
            return And(
                to_nnf(Not(operand.left)),
                to_nnf(Not(operand.right))
            )

    raise ValueError(
        "A fórmula precisa ter → e ↔ eliminados antes da FNN."
    )


def distribute_or_over_and(formula):
    """
    Distribui OR (∨) sobre AND (∧).

    Equivalência utilizada:
    A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C)
    """

    # Variáveis e literais negados não precisam ser alterados
    if isinstance(formula, Variable):
        return formula

    if isinstance(formula, Not):
        return formula

    # Processa os dois lados da conjunção
    if isinstance(formula, And):
        return And(
            distribute_or_over_and(formula.left),
            distribute_or_over_and(formula.right)
        )

    if isinstance(formula, Or):
        left = distribute_or_over_and(formula.left)
        right = distribute_or_over_and(formula.right)

        # (A ∧ B) ∨ C
        # vira
        # (A ∨ C) ∧ (B ∨ C)
        if isinstance(left, And):
            return And(
                distribute_or_over_and(
                    Or(left.left, right)
                ),
                distribute_or_over_and(
                    Or(left.right, right)
                )
            )

        # A ∨ (B ∧ C)
        # vira
        # (A ∨ B) ∧ (A ∨ C)
        if isinstance(right, And):
            return And(
                distribute_or_over_and(
                    Or(left, right.left)
                ),
                distribute_or_over_and(
                    Or(left, right.right)
                )
            )

        return Or(left, right)

    raise TypeError("Tipo de fórmula desconhecido.")


def to_cnf(formula):
    """
    Executa todas as etapas da conversão para FNC.

    1. Elimina → e ↔
    2. Converte para FNN
    3. Distribui ∨ sobre ∧
    """

    sem_implicacoes = eliminate_implications(formula)
    fnn = to_nnf(sem_implicacoes)
    fnc = distribute_or_over_and(fnn)

    return fnc


def literal_to_string(formula):
    """
    Converte um literal para texto.
    """

    if isinstance(formula, Variable):
        return formula.name

    if (
        isinstance(formula, Not)
        and isinstance(formula.operand, Variable)
    ):
        return f"¬{formula.operand.name}"

    raise ValueError("A fórmula recebida não é um literal.")


def clause_to_list(formula):
    """
    Converte uma cláusula em uma lista de literais.

    Exemplo:
    P ∨ ¬Q ∨ R

    vira:

    ["P", "¬Q", "R"]
    """

    if isinstance(formula, Or):
        return (
            clause_to_list(formula.left)
            + clause_to_list(formula.right)
        )

    return [literal_to_string(formula)]


def cnf_to_clauses(formula):
    """
    Converte uma fórmula em FNC para uma lista de cláusulas.

    Exemplo:

    (P ∨ Q) ∧ (¬P ∨ R)

    vira:

    [
        ["P", "Q"],
        ["¬P", "R"]
    ]
    """

    if isinstance(formula, And):
        return (
            cnf_to_clauses(formula.left)
            + cnf_to_clauses(formula.right)
        )

    return [clause_to_list(formula)]


def cnf_steps(formula):
    """
    Retorna todas as etapas da conversão para FNC.

    Isso será útil para mostrar o processo
    durante a apresentação do projeto.
    """

    sem_implicacoes = eliminate_implications(formula)

    fnn = to_nnf(sem_implicacoes)

    fnc = distribute_or_over_and(fnn)

    clausulas = cnf_to_clauses(fnc)

    return {
        "original": formula,
        "sem_implicacoes": sem_implicacoes,
        "fnn": fnn,
        "fnc": fnc,
        "clausulas": clausulas
    }