from src.formula import Variable, Not, And, Or, Implies, Iff


# Variáveis proposicionais
B = Variable("B")
M = Variable("M")
C = Variable("C")
I = Variable("I")
E = Variable("E")
P = Variable("P")


# Regras do diagnóstico

regra1 = Implies(
    And(B, E),
    M
)

regra2 = Implies(
    And(
        And(
            And(M, C),
            I
        ),
        E
    ),
    P
)

regra3 = Implies(P, M)
regra4 = Implies(P, C)
regra5 = Implies(P, I)


print("=== Diagnóstico Lógico de Partida ===")
print()

print("Regra 1:", regra1)
print("Regra 2:", regra2)
print("Regra 3:", regra3)
print("Regra 4:", regra4)
print("Regra 5:", regra5)