import customtkinter as ctk
from PIL import Image
from src.formula import Iff
from src.r4_cnf import cnf_steps
from pathlib import Path
from src.diagnostico import (
    analisar_estado,
    SISTEMA,
    SISTEMA_INSATISFATIVEL
)

from src.r3_solver import (
    find_models,
    classify,
    get_variables
)

# ============================================================
# CONFIGURAÇÃO GERAL
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#080C12"
SIDEBAR = "#0C1119"
CARD = "#101720"
CARD_2 = "#141D28"
BORDER = "#1E2A38"

TEXT = "#F5F7FA"
TEXT_MUTED = "#8492A6"

BLUE = "#1E9BFF"
BLUE_DARK = "#0C67B5"
GREEN = "#32D583"
YELLOW = "#F5C451"
RED = "#FF5A65"
BASE_DIR = Path(__file__).resolve().parent
CAR_PATH = BASE_DIR / "assets" / "car.png"

app = ctk.CTk()

app.title("LogicDrive - Diagnóstico Lógico Automotivo")
app.geometry("1360x820")
app.minsize(1150, 700)
app.configure(fg_color=BG)


# ============================================================
# GRID PRINCIPAL
# ============================================================

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)


# ============================================================
# SIDEBAR
# ============================================================
CENARIOS = {
    "Tudo funcionando": {
        "B": True,
        "M": True,
        "C": True,
        "I": True,
        "E": True,
        "P": True,
    },

    "Bateria descarregada": {
        "B": False,
        "M": False,
        "C": True,
        "I": True,
        "E": True,
        "P": False,
    },

    "ECU bloqueada": {
        "B": True,
        "M": False,
        "C": True,
        "I": True,
        "E": False,
        "P": False,
    },

    "Motor de partida com falha": {
        "B": True,
        "M": False,
        "C": True,
        "I": True,
        "E": True,
        "P": False,
    },

    "Sem combustível": {
        "B": True,
        "M": True,
        "C": False,
        "I": True,
        "E": True,
        "P": False,
    },

    "Falha de ignição": {
        "B": True,
        "M": True,
        "C": True,
        "I": False,
        "E": True,
        "P": False,
    },

    "Estado impossível / UNSAT": {
        "B": True,
        "M": False,
        "C": True,
        "I": True,
        "E": True,
        "P": True,
    },
}
sidebar = ctk.CTkFrame(
    app,
    width=205,
    corner_radius=0,
    fg_color=SIDEBAR
)

sidebar.grid(
    row=0,
    column=0,
    sticky="nsew"
)

sidebar.grid_propagate(False)


logo = ctk.CTkLabel(
    sidebar,
    text="LOGICDRIVE",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=24,
        weight="bold"
    ),
    text_color=TEXT
)

logo.pack(
    padx=22,
    pady=(30, 2),
    anchor="w"
)


logo_sub = ctk.CTkLabel(
    sidebar,
    text="LÓGICA AUTOMOTIVA",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=10,
        weight="bold"
    ),
    text_color=BLUE
)

logo_sub.pack(
    padx=24,
    pady=(0, 34),
    anchor="w"
)


def criar_botao_menu(texto, selecionado=False):

    if selecionado:
        fg = "#12365A"
        hover = "#184873"
        cor_texto = "#FFFFFF"
    else:
        fg = "transparent"
        hover = "#141D28"
        cor_texto = TEXT_MUTED

    botao = ctk.CTkButton(
        sidebar,
        text=texto,
        width=165,
        height=44,
        corner_radius=9,
        fg_color=fg,
        hover_color=hover,
        text_color=cor_texto,
        anchor="w",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=13,
            weight="bold"
        )
    )

    botao.pack(
        padx=18,
        pady=5
    )

    return botao


criar_botao_menu("⌂   Diagnóstico", True)
criar_botao_menu("◈   Modelos")
criar_botao_menu("⌘   Lógica")
criar_botao_menu("ƒ   FNC")
criar_botao_menu("≡   Histórico")


versao = ctk.CTkLabel(
    sidebar,
    text=(
        "LogicDrive v1.0\n"
        "Projeto de Lógica Computacional"
    ),
    justify="left",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=10
    ),
    text_color="#566273"
)

versao.pack(
    side="bottom",
    padx=22,
    pady=22,
    anchor="w"
)


# ============================================================
# CONTEÚDO PRINCIPAL
# ============================================================

conteudo = ctk.CTkFrame(
    app,
    fg_color=BG,
    corner_radius=0
)

conteudo.grid(
    row=0,
    column=1,
    sticky="nsew"
)

conteudo.grid_columnconfigure(0, weight=3)
conteudo.grid_columnconfigure(1, weight=2)
conteudo.grid_rowconfigure(1, weight=1)


# ============================================================
# HEADER
# ============================================================

header = ctk.CTkFrame(
    conteudo,
    height=82,
    fg_color=BG,
    corner_radius=0
)

header.grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="ew",
    padx=26
)


titulo = ctk.CTkLabel(
    header,
    text="Diagnóstico do Veículo",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=23,
        weight="bold"
    ),
    text_color=TEXT
)

titulo.pack(
    side="left",
    pady=(23, 0)
)


status_online = ctk.CTkLabel(
    header,
    text="●  SISTEMA ONLINE",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=11,
        weight="bold"
    ),
    text_color=GREEN
)

status_online.pack(
    side="right",
    pady=(25, 0)
)


# ============================================================
# PAINEL CENTRAL DO CARRO
# ============================================================

painel_carro = ctk.CTkFrame(
    conteudo,
    fg_color=CARD,
    corner_radius=16,
    border_width=1,
    border_color=BORDER
)

painel_carro.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=(26, 10),
    pady=(5, 12)
)

painel_carro.grid_rowconfigure(1, weight=1)
painel_carro.grid_columnconfigure(0, weight=1)


scan_header = ctk.CTkLabel(
    painel_carro,
    text="ESCANEAMENTO DO VEÍCULO",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=12,
        weight="bold"
    ),
    text_color=BLUE
)

scan_header.grid(
    row=0,
    column=0,
    sticky="w",
    padx=24,
    pady=(20, 0)
)


area_carro = ctk.CTkFrame(
    painel_carro,
    fg_color="#0B1119",
    corner_radius=13,
    border_width=1,
    border_color="#182536"
)

area_carro.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=20,
    pady=18
)


imagem_carro = ctk.CTkImage(
    light_image=Image.open(CAR_PATH),
    dark_image=Image.open(CAR_PATH),
    size=(620, 350)
)

carro_label = ctk.CTkLabel(
    area_carro,
    image=imagem_carro,
    text=""
)

carro_label.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)
# Linha luminosa usada durante o escaneamento
linha_scanner = ctk.CTkFrame(
    area_carro,
    height=3,
    fg_color=BLUE,
    corner_radius=2
)

# Começa escondida
linha_scanner.place_forget()


scan_texto = ctk.CTkLabel(
    painel_carro,
    text="VEÍCULO AGUARDANDO DIAGNÓSTICO",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=14,
        weight="bold"
    ),
    text_color=TEXT
)

scan_texto.grid(
    row=2,
    column=0,
    pady=(0, 8)
)


barra_progresso = ctk.CTkProgressBar(
    painel_carro,
    height=9,
    corner_radius=10,
    progress_color=BLUE,
    fg_color="#1A2837"
)

barra_progresso.grid(
    row=3,
    column=0,
    sticky="ew",
    padx=45,
    pady=(0, 9)
)

barra_progresso.set(0)


porcentagem = ctk.CTkLabel(
    painel_carro,
    text="0%",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=12,
        weight="bold"
    ),
    text_color=TEXT_MUTED
)

porcentagem.grid(
    row=4,
    column=0,
    pady=(0, 19)
)


# ============================================================
# PAINEL DE SISTEMAS
# ============================================================

painel_sistemas = ctk.CTkFrame(
    conteudo,
    fg_color=CARD,
    corner_radius=16,
    border_width=1,
    border_color=BORDER
)

painel_sistemas.grid(
    row=1,
    column=1,
    sticky="nsew",
    padx=(10, 26),
    pady=(5, 12)
)


titulo_sistemas = ctk.CTkLabel(
    painel_sistemas,
    text="STATUS DOS SISTEMAS",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=16,
        weight="bold"
    ),
    text_color=TEXT
)

titulo_sistemas.pack(
    padx=20,
    pady=(20, 2),
    anchor="w"
)


sub_sistemas = ctk.CTkLabel(
    painel_sistemas,
    text="Verificação lógica em tempo real",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=11
    ),
    text_color=TEXT_MUTED
)

sub_sistemas.pack(
    padx=20,
    pady=(0, 15),
    anchor="w"
)
cenario_selecionado = ctk.StringVar(
    value="Falha de ignição"
)

seletor_cenario = ctk.CTkComboBox(
    painel_sistemas,
    values=list(CENARIOS.keys()),
    variable=cenario_selecionado,
    height=36,
    corner_radius=8,
    fg_color="#141D28",
    border_color="#29425F",
    button_color=BLUE_DARK,
    button_hover_color=BLUE,
    dropdown_fg_color="#141D28",
    dropdown_hover_color="#1D3048",
    text_color=TEXT,
    font=ctk.CTkFont(
        family="Segoe UI",
        size=11
    )
)

seletor_cenario.pack(
    fill="x",
    padx=17,
    pady=(0, 10)
)


status_labels = {}


def criar_sistema(nome, descricao):

    card = ctk.CTkFrame(
        painel_sistemas,
        height=66,
        fg_color=CARD_2,
        corner_radius=11,
        border_width=1,
        border_color="#202D3D"
    )

    card.pack(
        fill="x",
        padx=17,
        pady=6
    )

    card.pack_propagate(False)


    textos = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    textos.pack(
        side="left",
        padx=16,
        pady=10
    )


    nome_label = ctk.CTkLabel(
        textos,
        text=nome,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=13,
            weight="bold"
        ),
        text_color=TEXT
    )

    nome_label.pack(anchor="w")


    descricao_label = ctk.CTkLabel(
        textos,
        text=descricao,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=10
        ),
        text_color=TEXT_MUTED
    )

    descricao_label.pack(anchor="w")


    status_label = ctk.CTkLabel(
        card,
        width=95,
        height=30,
        corner_radius=8,
        text="AGUARDANDO",
        fg_color="#1A2531",
        text_color=TEXT_MUTED,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=10,
            weight="bold"
        )
    )

    status_label.pack(
        side="right",
        padx=13
    )


    status_labels[nome] = status_label


criar_sistema(
    "Bateria",
    "Alimentação elétrica"
)

criar_sistema(
    "ECU",
    "Unidade de controle"
)

criar_sistema(
    "Motor de Partida",
    "Sistema de acionamento"
)

criar_sistema(
    "Combustível",
    "Fornecimento do motor"
)

criar_sistema(
    "Ignição",
    "Sistema de ignição"
)


# ============================================================
# CARD DE DIAGNÓSTICO
# ============================================================

resultado = ctk.CTkFrame(
    conteudo,
    fg_color=CARD,
    corner_radius=16,
    border_width=1,
    border_color=BORDER
)

resultado.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="ew",
    padx=26,
    pady=(0, 25)
)


resultado_textos = ctk.CTkFrame(
    resultado,
    fg_color="transparent"
)

resultado_textos.pack(
    side="left",
    padx=24,
    pady=20
)


resultado_titulo = ctk.CTkLabel(
    resultado_textos,
    text="Aguardando diagnóstico",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=20,
        weight="bold"
    ),
    text_color=TEXT
)

resultado_titulo.pack(anchor="w")


resultado_descricao = ctk.CTkLabel(
    resultado_textos,
    text="Execute uma análise para verificar o estado lógico do veículo.",
    font=ctk.CTkFont(
        family="Segoe UI",
        size=11
    ),
    text_color=TEXT_MUTED
)

resultado_descricao.pack(
    anchor="w",
    pady=(4, 0)
)


botoes_resultado = ctk.CTkFrame(
    resultado,
    fg_color="transparent"
)

botoes_resultado.pack(
    side="right",
    padx=20
)


def acao_temporaria():
    print("Função será conectada à lógica posteriormente.")


botao_logica = ctk.CTkButton(
    botoes_resultado,
    text="VER LÓGICA",
    width=115,
    height=39,
    corner_radius=9,
    fg_color="#152234",
    hover_color="#1D3048",
    border_width=1,
    border_color="#29425F",
    command=lambda: mostrar_logica()
)

botao_logica.pack(
    side="left",
    padx=5
)


botao_modelos = ctk.CTkButton(
    botoes_resultado,
    text="MODELOS",
    width=105,
    height=39,
    corner_radius=9,
    fg_color="#152234",
    hover_color="#1D3048",
    border_width=1,
    border_color="#29425F",
  command=lambda: mostrar_modelos()
)

botao_modelos.pack(
    side="left",
    padx=5
)


botao_fnc = ctk.CTkButton(
    botoes_resultado,
    text="VER FNC",
    width=105,
    height=39,
    corner_radius=9,
    fg_color="#152234",
    hover_color="#1D3048",
    border_width=1,
    border_color="#29425F",
    command=lambda: mostrar_fnc()
)

botao_fnc.pack(
    side="left",
    padx=5
)


botao_iniciar = ctk.CTkButton(
    botoes_resultado,
    text="▶  INICIAR DIAGNÓSTICO",
    width=190,
    height=42,
    corner_radius=10,
    fg_color=BLUE,
    hover_color=BLUE_DARK,
    font=ctk.CTkFont(
        family="Segoe UI",
        size=12,
        weight="bold"
    ),
    command=lambda: iniciar_diagnostico()
)

botao_iniciar.pack(
    side="left",
    padx=(10, 0)
)
def animar_scanner(posicao=0.15, direcao=1):
    """
    Move a linha azul verticalmente sobre o veículo.
    """

    linha_scanner.place(
        relx=0.5,
        rely=posicao,
        relwidth=0.92,
        anchor="center"
    )

    # Movimento
    posicao += 0.012 * direcao

    # Chegou embaixo: volta para cima
    if posicao >= 0.85:
        direcao = -1

    # Chegou em cima: desce novamente
    elif posicao <= 0.15:
        direcao = 1

    app.after(
        16,
        lambda: animar_scanner(posicao, direcao)
    )

# ============================================================
# EXECUTA
# ============================================================
scanner_ativo = False


def animar_scanner(posicao=0.15, direcao=1):
    global scanner_ativo

    if not scanner_ativo:
        linha_scanner.place_forget()
        return

    linha_scanner.place(
        relx=0.5,
        rely=posicao,
        relwidth=0.92,
        anchor="center"
    )

    posicao += 0.012 * direcao

    if posicao >= 0.85:
        direcao = -1
    elif posicao <= 0.15:
        direcao = 1

    app.after(
        16,
        lambda: animar_scanner(posicao, direcao)
    )


sistemas_diagnostico = [
    "Bateria",
    "ECU",
    "Motor de Partida",
    "Combustível",
    "Ignição"
]
VARIAVEL_SISTEMA = {
    "Bateria": "B",
    "ECU": "E",
    "Motor de Partida": "M",
    "Combustível": "C",
    "Ignição": "I",
}

valores_atuais = {}

def iniciar_diagnostico():
    global scanner_ativo
    global valores_atuais

    nome_cenario = cenario_selecionado.get()

    valores_atuais = CENARIOS[nome_cenario].copy()

    scanner_ativo = True

    botao_iniciar.configure(
        state="disabled",
        text="ANALISANDO..."
    )

    scan_texto.configure(
        text="ANALISANDO SISTEMAS...",
        text_color=BLUE
    )

    resultado_titulo.configure(
        text="Diagnóstico em andamento",
        text_color=TEXT
    )

    resultado_descricao.configure(
        text="Aplicando as regras lógicas aos sistemas do veículo."
    )

    barra_progresso.set(0)

    porcentagem.configure(
        text="0%"
    )

    # Limpa os estados anteriores
    for nome in sistemas_diagnostico:
        status_labels[nome].configure(
            text="AGUARDANDO",
            fg_color="#1A2531",
            text_color=TEXT_MUTED
        )

    animar_scanner()

    analisar_sistema(0)

def analisar_sistema(indice):
    if indice >= len(sistemas_diagnostico):
        finalizar_animacao()
        return

    nome = sistemas_diagnostico[indice]

    status_labels[nome].configure(
        text="ANALISANDO",
        fg_color="#4A3A14",
        text_color=YELLOW
    )

    progresso = indice / len(sistemas_diagnostico)

    barra_progresso.set(progresso)

    porcentagem.configure(
        text=f"{int(progresso * 100)}%"
    )

    app.after(
        850,
        lambda: concluir_sistema(indice)
    )
   
def concluir_sistema(indice):
    nome = sistemas_diagnostico[indice]

    # Descobre qual variável lógica representa este sistema
    variavel = VARIAVEL_SISTEMA[nome]

    # Se o valor da variável for False, o sistema está em falha
    falhou = not valores_atuais[variavel]

    if falhou:
        status_labels[nome].configure(
            text="✕  FALHA",
            fg_color="#451C22",
            text_color=RED
        )
    else:
        status_labels[nome].configure(
            text="✓  OK",
            fg_color="#153827",
            text_color=GREEN
        )

    # Atualiza o progresso
    progresso = (indice + 1) / len(sistemas_diagnostico)

    barra_progresso.set(progresso)

    porcentagem.configure(
        text=f"{int(progresso * 100)}%"
    )

    # Continua para o próximo sistema
    app.after(
        350,
        lambda: analisar_sistema(indice + 1)
    )
def finalizar_animacao():
    global scanner_ativo

    scanner_ativo = False
    linha_scanner.place_forget()

    # Analisa o estado usando o R5 real
    analise = analisar_estado(valores_atuais)

    falhas = []

    for nome in sistemas_diagnostico:
        variavel = VARIAVEL_SISTEMA[nome]

        if not valores_atuais[variavel]:
            falhas.append(nome)

    # Estado inconsistente com as regras lógicas
    if cenario_selecionado.get() == "Estado impossível / UNSAT":
        scan_texto.configure(
            text="INCONSISTÊNCIA LÓGICA DETECTADA",
            text_color=RED
        )

        resultado_titulo.configure(
            text="Estado impossível / inconsistente",
            text_color=RED
        )

        if analise["mensagens"]:
            resultado_descricao.configure(
                text=analise["mensagens"][0]
            )
        else:
            resultado_descricao.configure(
                text="O estado informado viola as regras lógicas do sistema."
            )

    # Algum sistema está em falha
    elif falhas:
        scan_texto.configure(
            text="DIAGNÓSTICO CONCLUÍDO",
            text_color=RED
        )

        if len(falhas) == 1:
            resultado_titulo.configure(
                text=f"Falha detectada: {falhas[0]}",
                text_color=RED
            )

            resultado_descricao.configure(
                text="O sistema indicado não atende às condições necessárias para a partida."
            )
        else:
            resultado_titulo.configure(
                text=f"{len(falhas)} falhas detectadas",
                text_color=RED
            )

            resultado_descricao.configure(
                text="Sistemas: " + ", ".join(falhas)
            )

    # Tudo funcionando
    else:
        scan_texto.configure(
            text="DIAGNÓSTICO CONCLUÍDO",
            text_color=GREEN
        )

        resultado_titulo.configure(
            text="Veículo pronto para partida",
            text_color=GREEN
        )

        resultado_descricao.configure(
            text="Todas as condições lógicas necessárias foram satisfeitas."
        )

    barra_progresso.set(1)

    porcentagem.configure(
        text="100%"
    )

    botao_iniciar.configure(
        state="normal",
        text="▶  EXECUTAR NOVAMENTE"
    )

def mostrar_logica():
    # Usa o cenário atual mesmo que o diagnóstico ainda não tenha sido executado
    valores = (
        valores_atuais
        if valores_atuais
        else CENARIOS[cenario_selecionado.get()]
    )

    B = valores["B"]
    M = valores["M"]
    C = valores["C"]
    I = valores["I"]
    E = valores["E"]
    P = valores["P"]

    def vf(valor):
        return "V" if valor else "F"

    # Avalia as mesmas regras utilizadas pelo diagnóstico
    regras = [
        (
            "(B ∧ E) → M",
            (not (B and E)) or M
        ),
        (
            "(M ∧ C ∧ I ∧ E) → P",
            (not (M and C and I and E)) or P
        ),
        (
            "P → M",
            (not P) or M
        ),
        (
            "P → C",
            (not P) or C
        ),
        (
            "P → I",
            (not P) or I
        ),
    ]

    janela_logica = ctk.CTkToplevel(app)

    janela_logica.title("LogicDrive - Análise Lógica")
    janela_logica.geometry("760x650")
    janela_logica.resizable(False, False)
    janela_logica.configure(fg_color=BG)

    # Mantém a janela na frente da principal
    janela_logica.transient(app)
    janela_logica.grab_set()


    titulo = ctk.CTkLabel(
        janela_logica,
        text="RACIOCÍNIO LÓGICO",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=24,
            weight="bold"
        ),
        text_color=TEXT
    )

    titulo.pack(
        padx=30,
        pady=(28, 3),
        anchor="w"
    )


    subtitulo = ctk.CTkLabel(
        janela_logica,
        text=f"Cenário: {cenario_selecionado.get()}",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=12
        ),
        text_color=TEXT_MUTED
    )

    subtitulo.pack(
        padx=30,
        pady=(0, 20),
        anchor="w"
    )


    # ========================================================
    # VALORAÇÃO
    # ========================================================

    card_valores = ctk.CTkFrame(
        janela_logica,
        fg_color=CARD,
        corner_radius=14,
        border_width=1,
        border_color=BORDER
    )

    card_valores.pack(
        fill="x",
        padx=30,
        pady=(0, 14)
    )


    titulo_valores = ctk.CTkLabel(
        card_valores,
        text="VALORAÇÃO ATUAL",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=14,
            weight="bold"
        ),
        text_color=BLUE
    )

    titulo_valores.pack(
        padx=20,
        pady=(16, 8),
        anchor="w"
    )


    texto_valores = (
        f"Bateria (B)              {vf(B)}\n"
        f"ECU (E)                  {vf(E)}\n"
        f"Motor de Partida (M)     {vf(M)}\n"
        f"Combustível (C)          {vf(C)}\n"
        f"Ignição (I)              {vf(I)}\n"
        f"Motor funcionando (P)    {vf(P)}"
    )


    valores_label = ctk.CTkLabel(
        card_valores,
        text=texto_valores,
        justify="left",
        font=ctk.CTkFont(
            family="Consolas",
            size=13
        ),
        text_color=TEXT
    )

    valores_label.pack(
        padx=20,
        pady=(0, 18),
        anchor="w"
    )


    # ========================================================
    # REGRAS
    # ========================================================

    card_regras = ctk.CTkFrame(
        janela_logica,
        fg_color=CARD,
        corner_radius=14,
        border_width=1,
        border_color=BORDER
    )

    card_regras.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )


    titulo_regras = ctk.CTkLabel(
        card_regras,
        text="REGRAS DO SISTEMA",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=14,
            weight="bold"
        ),
        text_color=BLUE
    )

    titulo_regras.pack(
        padx=20,
        pady=(16, 10),
        anchor="w"
    )


    for formula, resultado in regras:

        linha = ctk.CTkFrame(
            card_regras,
            fg_color=CARD_2,
            corner_radius=9
        )

        linha.pack(
            fill="x",
            padx=18,
            pady=5
        )


        formula_label = ctk.CTkLabel(
            linha,
            text=formula,
            font=ctk.CTkFont(
                family="Consolas",
                size=13,
                weight="bold"
            ),
            text_color=TEXT
        )

        formula_label.pack(
            side="left",
            padx=14,
            pady=11
        )


        resultado_label = ctk.CTkLabel(
            linha,
            text="✓ VERDADEIRA" if resultado else "✕ FALSA",
            text_color=GREEN if resultado else RED,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
                weight="bold"
            )
        )

        resultado_label.pack(
            side="right",
            padx=14
        )

def mostrar_modelos():
    nome_cenario = cenario_selecionado.get()

    # No cenário especial, usamos a fórmula propositalmente insatisfatível
    if nome_cenario == "Estado impossível / UNSAT":
        formula = SISTEMA_INSATISFATIVEL
    else:
        formula = SISTEMA

    # Usa diretamente as funções do R3
    modelos = find_models(formula)
    classificacao = classify(formula)
    variaveis = sorted(get_variables(formula))

    total_valoracoes = 2 ** len(variaveis)

    # Usa a valoração atual do diagnóstico
    valores = (
        valores_atuais
        if valores_atuais
        else CENARIOS[nome_cenario]
    )

    valoracao_atual_satisfaz = formula.evaluate(valores)

    status_sat = "SAT" if modelos else "UNSAT"

    # ========================================================
    # JANELA
    # ========================================================

    janela_modelos = ctk.CTkToplevel(app)

    janela_modelos.title("LogicDrive - Modelos e SAT")
    janela_modelos.geometry("820x700")
    janela_modelos.resizable(False, False)
    janela_modelos.configure(fg_color=BG)

    janela_modelos.transient(app)
    janela_modelos.grab_set()

    titulo = ctk.CTkLabel(
        janela_modelos,
        text="MODELOS E SAT",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=24,
            weight="bold"
        ),
        text_color=TEXT
    )

    titulo.pack(
        padx=30,
        pady=(28, 3),
        anchor="w"
    )

    subtitulo = ctk.CTkLabel(
        janela_modelos,
        text=f"Cenário: {nome_cenario}",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=12
        ),
        text_color=TEXT_MUTED
    )

    subtitulo.pack(
        padx=30,
        pady=(0, 20),
        anchor="w"
    )

    # ========================================================
    # RESUMO
    # ========================================================

    resumo = ctk.CTkFrame(
        janela_modelos,
        fg_color=CARD,
        corner_radius=14,
        border_width=1,
        border_color=BORDER
    )

    resumo.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    status_cor = GREEN if modelos else RED

    status = ctk.CTkLabel(
        resumo,
        text=status_sat,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=26,
            weight="bold"
        ),
        text_color=status_cor
    )

    status.pack(
        padx=20,
        pady=(18, 4),
        anchor="w"
    )

    info = ctk.CTkLabel(
        resumo,
        text=(
            f"Classificação: {classificacao.upper()}\n"
            f"Modelos encontrados: {len(modelos)} / {total_valoracoes}\n"
            f"Variáveis: {len(variaveis)}"
        ),
        justify="left",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=12
        ),
        text_color=TEXT
    )

    info.pack(
        padx=20,
        pady=(0, 10),
        anchor="w"
    )

    if valoracao_atual_satisfaz:
        texto_atual = "✓ A valoração atual É um modelo da fórmula."
        cor_atual = GREEN
    else:
        texto_atual = "✕ A valoração atual NÃO satisfaz a fórmula."
        cor_atual = RED

    valoracao_label = ctk.CTkLabel(
        resumo,
        text=texto_atual,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=11,
            weight="bold"
        ),
        text_color=cor_atual
    )

    valoracao_label.pack(
        padx=20,
        pady=(0, 18),
        anchor="w"
    )

    # ========================================================
    # LISTA DOS MODELOS
    # ========================================================

    area_modelos = ctk.CTkFrame(
        janela_modelos,
        fg_color=CARD,
        corner_radius=14,
        border_width=1,
        border_color=BORDER
    )

    area_modelos.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )

    titulo_lista = ctk.CTkLabel(
        area_modelos,
        text="MODELOS ENCONTRADOS",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=14,
            weight="bold"
        ),
        text_color=BLUE
    )

    titulo_lista.pack(
        padx=20,
        pady=(16, 10),
        anchor="w"
    )

    if not modelos:

        nenhum = ctk.CTkLabel(
            area_modelos,
            text=(
                "Nenhum modelo satisfaz todas as restrições.\n\n"
                "A fórmula é insatisfatível."
            ),
            justify="center",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold"
            ),
            text_color=RED
        )

        nenhum.pack(
            expand=True
        )

        return

    tabela = ctk.CTkTextbox(
        area_modelos,
        fg_color="#0B1119",
        text_color=TEXT,
        font=ctk.CTkFont(
            family="Consolas",
            size=13
        ),
        corner_radius=10
    )

    tabela.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=(0, 18)
    )

    # Cabeçalho
    tabela.insert(
        "end",
        " | ".join(variaveis) + "\n"
    )

    tabela.insert(
        "end",
        "-" * (len(variaveis) * 4) + "\n"
    )

    # Modelos
    for indice, modelo in enumerate(modelos, start=1):

        valores_linha = []

        for variavel in variaveis:
            valor = "V" if modelo[variavel] else "F"
            valores_linha.append(valor)

        tabela.insert(
            "end",
            f"{indice:02d}.  " + " | ".join(valores_linha) + "\n"
        )

    tabela.configure(
        state="disabled"
    )

def mostrar_fnc():
    from src.formula import Variable, Not, And, Or, Implies, Iff

    nome_cenario = cenario_selecionado.get()

    # Usa a fórmula normal ou a fórmula impossível
    if nome_cenario == "Estado impossível / UNSAT":
        formula = SISTEMA_INSATISFATIVEL
    else:
        formula = SISTEMA

    # Executa o R4 de verdade
    etapas = cnf_steps(formula)

    # --------------------------------------------------------
    # Converte a árvore da fórmula para um texto mais bonito
    # --------------------------------------------------------                                              
    def formula_texto(f):
        if isinstance(f, Variable):
            return f.name

        if isinstance(f, Not):
            if isinstance(f.operand, Variable):
                return f"¬{formula_texto(f.operand)}"

            return f"¬({formula_texto(f.operand)})"

        if isinstance(f, And):
            return (
                f"({formula_texto(f.left)} "
                f"∧ {formula_texto(f.right)})"
            )

        if isinstance(f, Or):
            return (
                f"({formula_texto(f.left)} "
                f"∨ {formula_texto(f.right)})"
            )

        if isinstance(f, Implies):
            return (
                f"({formula_texto(f.left)} "
                f"→ {formula_texto(f.right)})"
            )

        if isinstance(f, Iff):
            return (
                f"({formula_texto(f.left)} "
                f"↔ {formula_texto(f.right)})"
            )

        return str(f)

    janela_fnc = ctk.CTkToplevel(app)

    janela_fnc = ctk.CTkToplevel(app)

    janela_fnc.title("LogicDrive - Conversão para FNC")

    janela_fnc = ctk.CTkToplevel(app)

    janela_fnc.title("LogicDrive - Conversão para FNC")
    janela_fnc.geometry("900x760")
    janela_fnc.resizable(False, False)
    janela_fnc.configure(fg_color=BG)

    janela_fnc.transient(app)
    janela_fnc.grab_set()

    titulo = ctk.CTkLabel(
        janela_fnc,
        text="CONVERSÃO PARA FNC",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=24,
            weight="bold"
        ),
        text_color=TEXT
    )

    titulo.pack(
        padx=30,
        pady=(26, 2),
        anchor="w"
    )

    subtitulo = ctk.CTkLabel(
        janela_fnc,
        text=(
            "Forma Normal Conjuntiva • "
            f"Cenário: {nome_cenario}"
        ),
        font=ctk.CTkFont(
            family="Segoe UI",
            size=12
        ),
        text_color=TEXT_MUTED
    )

    subtitulo.pack(
        padx=30,
        pady=(0, 18),
        anchor="w"
    )

    # Área com rolagem
    area = ctk.CTkScrollableFrame(
        janela_fnc,
        fg_color=BG,
        corner_radius=0
    )

    area.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    # --------------------------------------------------------
    # FUNÇÃO PARA CRIAR CADA ETAPA
    # --------------------------------------------------------

    def adicionar_etapa(numero, titulo_etapa, descricao, conteudo):
        card = ctk.CTkFrame(
            area,
            fg_color=CARD,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            padx=10,
            pady=7
        )

        topo = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        topo.pack(
            fill="x",
            padx=18,
            pady=(14, 3)
        )

        numero_label = ctk.CTkLabel(
            topo,
            text=str(numero),
            width=30,
            height=30,
            corner_radius=15,
            fg_color=BLUE_DARK,
            text_color=TEXT,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold"
            )
        )

        numero_label.pack(
            side="left"
        )

        titulo_label = ctk.CTkLabel(
            topo,
            text=titulo_etapa,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=14,
                weight="bold"
            ),
            text_color=BLUE
        )

        titulo_label.pack(
            side="left",
            padx=10
        )

        descricao_label = ctk.CTkLabel(
            card,
            text=descricao,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11
            ),
            text_color=TEXT_MUTED
        )

        descricao_label.pack(
            padx=18,
            pady=(0, 8),
            anchor="w"
        )

        texto = ctk.CTkTextbox(
            card,
            height=85,
            fg_color="#0B1119",
            text_color=TEXT,
            border_width=0,
            corner_radius=9,
            wrap="word",
            font=ctk.CTkFont(
                family="Consolas",
                size=12
            )
        )

        texto.pack(
            fill="x",
            padx=18,
            pady=(0, 16)
        )

        texto.insert(
            "1.0",
            conteudo
        )

        texto.configure(
            state="disabled"
        )

    # --------------------------------------------------------
    # ETAPAS REAIS DO R4
    # --------------------------------------------------------

    adicionar_etapa(
        1,
        "FÓRMULA ORIGINAL",
        "Fórmula lógica antes de qualquer transformação.",
        formula_texto(etapas["original"])
    )

    adicionar_etapa(
        2,
        "ELIMINAÇÃO DAS IMPLICAÇÕES",
        "Substituímos A → B por ¬A ∨ B.",
        formula_texto(etapas["sem_implicacoes"])
    )

    adicionar_etapa(
        3,
        "FORMA NORMAL DA NEGAÇÃO",
        "As negações passam a aparecer somente sobre variáveis.",
        formula_texto(etapas["fnn"])
    )

    adicionar_etapa(
        4,
        "FORMA NORMAL CONJUNTIVA",
        "Distribuímos ∨ sobre ∧ até obter uma conjunção de cláusulas.",
        formula_texto(etapas["fnc"])
    )

    # --------------------------------------------------------
    # CLÁUSULAS
    # --------------------------------------------------------

    clausulas_texto = ""

    for indice, clausula in enumerate(
        etapas["clausulas"],
        start=1
    ):
        clausulas_texto += (
            f"C{indice:02d}:  "
            f"({' ∨ '.join(clausula)})\n"
        )

    adicionar_etapa(
        5,
        "CLÁUSULAS DA FNC",
        (
            f"Resultado final separado em "
            f"{len(etapas['clausulas'])} cláusulas."
        ),
        clausulas_texto
    )

app.mainloop()