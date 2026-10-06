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
    
    def size(self):
        return 1

    def variables(self):
        return {self.name}


class Not(Formula):
    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        return f"¬{self.operand}"

    def evaluate(self, values):
        return not self.operand.evaluate(values)

    def size(self):
        return 1 + self.operand.size()

    def variables(self):
        return self.operand.variables()

class And(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∧ {self.right})"

    def evaluate(self, values):
        return self.left.evaluate(values) and self.right.evaluate(values)

    def variables(self):
        return self.left.variables() | self.right.variables()

    def size(self):
        return 1 + self.left.size() + self.right.size()


class Or(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∨ {self.right})"

    def evaluate(self, values):
        return self.left.evaluate(values) or self.right.evaluate(values)

    def variables(self):
        return self.left.variables() | self.right.variables()

    def size(self):
        return 1 + self.left.size() + self.right.size()


class Implies(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} → {self.right})"

    def evaluate(self, values):
        return (not self.left.evaluate(values)) or self.right.evaluate(values)

    def variables(self):
            return self.left.variables() | self.right.variables()

    def size(self):
        return 1 + self.left.size() + self.right.size()


class Iff(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ↔ {self.right})"

    def evaluate(self, values):
        return self.left.evaluate(values) == self.right.evaluate(values)

    def variables(self):
        return self.left.variables() | self.right.variables()

    def size(self):
        return 1 + self.left.size() + self.right.size()