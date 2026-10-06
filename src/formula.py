class Formula:
    """Classe base para todas as fórmulas lógicas."""
    pass


class Variable(Formula):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Not(Formula):
    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        return f"¬{self.operand}"


class And(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∧ {self.right})"


class Or(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∨ {self.right})"


class Implies(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} → {self.right})"


class Iff(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ↔ {self.right})"