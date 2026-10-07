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


# Situação de teste
valores = {
    "B": True,
    "M": False,
    "C": True,
    "I": True,
    "E": True,
    "P": False
}


print("=== Diagnóstico Lógico de Partida ===")
print()

print("Regra 1:", regra1)
print("Regra 2:", regra2)
print("Regra 3:", regra3)
print("Regra 4:", regra4)
print("Regra 5:", regra5)

print()
print("=== Avaliação ===")

print("Regra 1:", regra1.evaluate(valores))
print("Regra 2:", regra2.evaluate(valores))
print("Regra 3:", regra3.evaluate(valores))
print("Regra 4:", regra4.evaluate(valores))
print("Regra 5:", regra5.evaluate(valores))

print()
print("=== Tamanho das Fórmulas ===")

print("Regra 1:", regra1.size(), "nós")
print("Regra 2:", regra2.size(), "nós")
print("Regra 3:", regra3.size(), "nós")
print("Regra 4:", regra4.size(), "nós")
print("Regra 5:", regra5.size(), "nós")

print()
print("=== Variáveis das Fórmulas ===")

print("Regra 1:", sorted(regra1.variables()))
print("Regra 2:", sorted(regra2.variables()))
print("Regra 3:", sorted(regra3.variables()))
print("Regra 4:", sorted(regra4.variables()))
print("Regra 5:", sorted(regra5.variables()))

#testa o diagnostico.py
from src.diagnostico import analisar_estado, DESCRICOES

estado = {
    "B": True,
    "M": False,
    "C": True,
    "I": True,
    "E": True,
    "P": False,
}

resultado = analisar_estado(estado)

print()
print("=== Diagnóstico do Veículo ===")

for variavel, valor in estado.items():
    descricao = DESCRICOES[variavel]
    resposta = "SIM" if valor else "NÃO"

    print(f"{descricao}: {resposta}")

print()

if resultado["consistente"]:
    print("Estado logicamente consistente.")
else:
    print("Estado logicamente inconsistente.")
    print("Regras violadas:")

    for regra in resultado["violadas"]:
        print("-", regra)


#importa o modulo diagnostico.py e r3.solver
from src.diagnostico import (
    analisar_estado,
    DESCRICOES,
    SISTEMA
)

from src.r3_solver import (
    classify,
    model_count,
    first_model
)

print()
print("=== Análise Lógica do Sistema ===")

print("Classificação:", classify(SISTEMA))
print("Quantidade de modelos:", model_count(SISTEMA))

modelo = first_model(SISTEMA)

if modelo is not None:
    print("Exemplo de estado válido:")

    for variavel, valor in modelo.items():
        descricao = DESCRICOES[variavel]
        resposta = "SIM" if valor else "NÃO"

        print(f"- {descricao}: {resposta}")



#importa o modulo diagnostico.py com o sistema insatisfativel
from src.diagnostico import (
    analisar_estado,
    DESCRICOES,
    SISTEMA,
    SISTEMA_INSATISFATIVEL
)


print()
print("=== Variante Insatisfatível ===")

print("Classificação:", classify(SISTEMA_INSATISFATIVEL))
print(
    "Quantidade de modelos:",
    model_count(SISTEMA_INSATISFATIVEL)
)

#mostra as mensagens amigáveis para o usuário
if resultado["consistente"]:
    print("Estado logicamente consistente.")
else:
    print("Estado logicicamente inconsistente.")

    for mensagem in resultado["mensagens"]:
        print("-", mensagem)