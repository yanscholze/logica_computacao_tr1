import tkinter as tk


# Cria a janela principal
janela = tk.Tk()

# Título da janela
janela.title("LogicDrive - Diagnóstico Lógico Automotivo")

# Tamanho inicial
janela.geometry("1000x650")

# Impede a janela de ficar pequena demais
janela.minsize(900, 600)

# Fundo escuro
janela.configure(bg="#101317")


# Título principal
titulo = tk.Label(
    janela,
    text="LOGICDRIVE",
    font=("Arial", 32, "bold"),
    fg="white",
    bg="#101317"
)

titulo.pack(pady=(40, 5))


# Subtítulo
subtitulo = tk.Label(
    janela,
    text="Sistema de Diagnóstico Lógico Automotivo",
    font=("Arial", 14),
    fg="#AAB2BD",
    bg="#101317"
)

subtitulo.pack()


# Texto central
status = tk.Label(
    janela,
    text="VEÍCULO AGUARDANDO DIAGNÓSTICO",
    font=("Arial", 18, "bold"),
    fg="#FFFFFF",
    bg="#101317"
)

status.pack(expand=True)
def iniciar_diagnostico():
    """
    Simula a análise dos sistemas do veículo
    um por um.
    """

    # Desativa o botão durante o diagnóstico
    botao_diagnostico.config(
        state="disabled",
        text="DIAGNÓSTICO EM ANDAMENTO..."
    )

    status.config(
        text="ANALISANDO SISTEMAS...",
        fg="#F5C542"
    )

    # Resultado provisório de cada sistema
    resultados = {
        "BATERIA": True,
        "ECU": True,
        "MOTOR DE PARTIDA": True,
        "COMBUSTÍVEL": True,
        "IGNIÇÃO": False
    }

    sistemas_lista = list(resultados.keys())

    def analisar_sistema(indice):
        # Quando terminar todos os sistemas
        if indice >= len(sistemas_lista):
            finalizar_diagnostico(resultados)
            return

        sistema = sistemas_lista[indice]
        label = status_sistemas[sistema]

        # Mostra que o sistema está sendo analisado
        label.config(
            text="● ANALISANDO...",
            fg="#F5C542"
        )

        # Espera um pouco e mostra o resultado
        janela.after(
            700,
            lambda: mostrar_resultado(
                sistema,
                resultados[sistema],
                indice
            )
        )

    def mostrar_resultado(sistema, resultado, indice):
        label = status_sistemas[sistema]

        if resultado:
            label.config(
                text="✓ OK",
                fg="#42D67B"
            )
        else:
            label.config(
                text="✗ FALHA",
                fg="#FF5252"
            )

        # Passa para o próximo sistema
        janela.after(
            500,
            lambda: analisar_sistema(indice + 1)
        )

    # Começa pelo primeiro sistema
    analisar_sistema(0)


def finalizar_diagnostico(resultados):
    """
    Exibe o resultado final do diagnóstico.
    """

    falhas = [
        sistema
        for sistema, resultado in resultados.items()
        if not resultado
    ]

    if len(falhas) == 0:
        status.config(
            text="SISTEMA APROVADO - MOTOR PRONTO PARA PARTIDA",
            fg="#42D67B"
        )
    else:
        status.config(
            text=f"FALHA DETECTADA: {falhas[0]}",
            fg="#FF5252"
        )

    botao_diagnostico.config(
        state="normal",
        text="EXECUTAR NOVAMENTE"
    )
    
# Painel com os sistemas analisados
painel = tk.Frame(
    janela,
    bg="#171B21",
    padx=30,
    pady=20
)

painel.pack(pady=20)


# Sistemas que serão verificados pelo LogicDrive
sistemas = [
    "BATERIA",
    "ECU",
    "MOTOR DE PARTIDA",
    "COMBUSTÍVEL",
    "IGNIÇÃO"
]


# Guarda os textos de status para podermos alterá-los depois
status_sistemas = {}


for sistema in sistemas:

    linha = tk.Frame(
        painel,
        bg="#171B21"
    )

    linha.pack(
        fill="x",
        pady=5
    )

    nome = tk.Label(
        linha,
        text=sistema,
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#171B21",
        width=22,
        anchor="w"
    )

    nome.pack(side="left")


    resultado = tk.Label(
        linha,
        text="● AGUARDANDO",
        font=("Arial", 11, "bold"),
        fg="#7A8594",
        bg="#171B21",
        width=18,
        anchor="e"
    )

    resultado.pack(side="right")

    # Guarda cada label usando o nome do sistema
    status_sistemas[sistema] = resultado

botao_diagnostico = tk.Button(
    janela,
    text="INICIAR DIAGNÓSTICO",
    font=("Arial", 14, "bold"),
    bg="#1E88E5",
    fg="white",
    activebackground="#1565C0",
    activeforeground="white",
    bd=0,
    padx=30,
    pady=15,
    cursor="hand2",
    command=iniciar_diagnostico
)

botao_diagnostico.pack(pady=(0, 50))

# Mantém a janela aberta
janela.mainloop()