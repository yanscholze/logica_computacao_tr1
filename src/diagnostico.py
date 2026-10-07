from src.formula import Variable, And, Implies, Not


# Variáveis do Diagnóstico
B = Variable("B")  # Bateria tem tensão adequada
M = Variable("M")  # Motor de arranque funciona
C = Variable("C")  # Combustível suficiente
I = Variable("I")  # Ignição funciona
E = Variable("E")  # ECU permite a partida
P = Variable("P")  # Motor funciona

#Regras do Sisitema
REGRA_BATERIA_PARTIDA = Implies(
    And(B, E),
    M
)

REGRA_FUNCIONAMENTO = Implies(
    And(
        And(
            And(M, C),
            I
        ),
        E
    ),
    P
)

REGRA_MOTOR_GIRANDO = Implies(P, M)
REGRA_COMBUSTIVEL = Implies(P, C)
REGRA_IGNICAO = Implies(P, I)


REGRAS = [
    REGRA_BATERIA_PARTIDA,
    REGRA_FUNCIONAMENTO,
    REGRA_MOTOR_GIRANDO,
    REGRA_COMBUSTIVEL,
    REGRA_IGNICAO,
]

#Descrições das variáveis
DESCRICOES = {
    "B": "Bateria possui tensão adequada",
    "M": "Motor de partida gira",
    "C": "Combustível disponível",
    "I": "Sistema de ignição funciona",
    "E": "ECU permite a partida",
    "P": "Motor entra em funcionamento",
}

#Define se teve alguma regra violada
def regras_violadas(valores):
    violadas = []

    for regra in REGRAS:
        if not regra.evaluate(valores):
            violadas.append(regra)

    return violadas

#Realiza a análise completa
def analisar_estado(valores):
    violadas = regras_violadas(valores)

    mensagens = []

    for regra in violadas:
        mensagens.append(MENSAGENS_REGRAS[regra])

    return {
        "consistente": len(violadas) == 0,
        "violadas": violadas,
        "mensagens": mensagens,
    }

#normaliza para a leitura do r3
SISTEMA = And(
    And(
        And(
            And(
                REGRA_BATERIA_PARTIDA,
                REGRA_FUNCIONAMENTO
            ),
            REGRA_MOTOR_GIRANDO
        ),
        REGRA_COMBUSTIVEL
    ),
    REGRA_IGNICAO
)

SISTEMA_INSATISFATIVEL = And(
    And(
        SISTEMA,
        P
    ),
    Not(M)
)


#importa o Not
from src.formula import Variable, And, Implies, Not


#insere textos amigáveis para as variáveis do sistema
MENSAGENS_REGRAS = {
    REGRA_BATERIA_PARTIDA:
        "A bateria possui tensão adequada e a ECU permite a partida, "
        "mas o motor de partida não gira.",

    REGRA_FUNCIONAMENTO:
        "O motor de partida gira, há combustível, a ignição funciona "
        "e a ECU permite a partida, mas o motor não entra em funcionamento.",

    REGRA_MOTOR_GIRANDO:
        "O motor foi informado como funcionando, mas o motor de partida "
        "foi informado como não girando.",

    REGRA_COMBUSTIVEL:
        "O motor foi informado como funcionando, mas não há combustível disponível.",

    REGRA_IGNICAO:
        "O motor foi informado como funcionando, mas o sistema de ignição "
        "foi informado como inoperante.",
}