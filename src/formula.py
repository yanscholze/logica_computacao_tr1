class Formula:
    """Classe base para todas as fórmulas lógicas."""
    pass


class Variable(Formula):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def evaluate(self, values):
        return values[self.name]


class Not(Formula):
    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        return f"¬{self.operand}"

    def evaluate(self, values):
        return not self.operand.evaluate(values)


class And(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∧ {self.right})"

    def evaluate(self, values):
        return self.left.evaluate(values) and self.right.evaluate(values)


class Or(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∨ {self.right})"

    def evaluate(self, values):
        return self.left.evaluate(values) or self.right.evaluate(values)


class Implies(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} → {self.right})"

    def evaluate(self, values):
        return (not self.left.evaluate(values)) or self.right.evaluate(values)


class Iff(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ↔ {self.right})"

    def evaluate(self, values):
        return self.left.evaluate(values) == self.right.evaluate(values)