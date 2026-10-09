# LogicDrive — Diagnóstico lógico automotivo

Projeto acadêmico de **Lógica para Computação**. O LogicDrive representa condições de partida de um veículo com lógica proposicional e usa essas fórmulas para avaliar estados, encontrar modelos e explicar quando um cenário é satisfatível.

## Interface gráfica

A interface completa está em `logicdrive_premium.py`. Ela permite escolher cenários, executar o diagnóstico e consultar modelos, regras, conversão para FNC e o histórico da sessão. `logicdrive.py` é um protótipo simples em Tkinter; `main.py` demonstra as operações no terminal.

O arquivo da interface já está na branch padrão `main` do repositório. Ao clonar o projeto, **não é necessário trocar para `felipe-ui-premium`**.

## O modelo lógico

| Símbolo | Significado |
| --- | --- |
| `B` | A bateria tem tensão adequada |
| `M` | O motor de partida gira |
| `C` | Há combustível |
| `I` | O sistema de ignição funciona |
| `E` | A ECU permite a partida |
| `P` | O motor entra em funcionamento |

O sistema usa as regras:

```text
(B ∧ E) → M
(M ∧ C ∧ I ∧ E) → P
P → M
P → C
P → I
```

Também há um cenário propositalmente inconsistente para demonstrar um conjunto de regras insatisfatível (UNSAT).

## Funcionalidades

- AST de fórmulas proposicionais com `¬`, `∧`, `∨`, `→` e `↔`;
- avaliação de fórmulas, identificação de variáveis e tamanho da AST;
- parser de fórmulas escritas em texto;
- busca e contagem de modelos e classificação SAT;
- conversão clássica para Forma Normal Conjuntiva (FNC);
- transformação de Tseitin, exportação DIMACS e solver DPLL;
- integração opcional com o solver PySAT;
- diagnóstico aplicado aos cenários automotivos da interface.

## Executar no Linux

### Fedora

Instale Python, `pip` e o suporte do Tkinter fornecido pelo sistema:

```bash
sudo dnf install python3 python3-pip python3-tkinter
```

Na pasta do projeto, crie um ambiente virtual e instale as bibliotecas da interface:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install customtkinter pillow
python logicdrive_premium.py
```

Use o ambiente virtual sempre que for iniciar a interface. Para ativá-lo novamente em outro terminal:

```bash
cd "/caminho/para/logica_computacao_tr1"
source .venv/bin/activate
python logicdrive_premium.py
```

O ambiente virtual instala sua própria versão do Pillow, incluindo `PIL.ImageTk`. Isso evita a separação desse módulo feita pelo pacote RPM do Fedora. Se optar por usar o Pillow do sistema fora de um ambiente virtual, instale também `sudo dnf install python3-pillow-tk`.

O código mantém `winsound` no Windows. No Linux, tenta tocar os arquivos WAV usando o primeiro programa disponível entre `pw-play`, `paplay`, `aplay` e `ffplay`. Se nenhum estiver instalado, a interface continua funcionando, mas sem efeitos sonoros.

### Ubuntu e Debian

Instale o Python, o suporte de ambientes virtuais e o Tkinter:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
```

Depois, siga os mesmos comandos de criação e ativação do ambiente virtual acima.

## Executar no Windows

Com Python instalado, abra o terminal na pasta do projeto e rode:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install customtkinter pillow
python logicdrive_premium.py
```

## Demonstração no terminal

Para executar os exemplos de lógica sem abrir a interface:

```bash
python main.py
```

## Testes

Com o ambiente virtual ativo, instale as dependências de desenvolvimento:

```bash
python -m pip install pytest python-sat
```

Execute a suíte:

```bash
python -m pytest -v
```

`python-sat` é necessário para os testes da integração com PySAT; a interface gráfica não depende desse solver externo.

## Estrutura do projeto

```text
├── assets/
│   ├── car.png
│   └── sounds/              # efeitos sonoros WAV
├── src/
│   ├── diagnostico.py       # regras e diagnóstico automotivo
│   ├── dpll.py              # solver DPLL
│   ├── formula.py           # AST e operadores lógicos
│   ├── parser.py            # parser de fórmulas
│   ├── r3_solver.py         # busca de modelos e classificação SAT
│   ├── r4_cnf.py            # conversão para FNC
│   ├── solver_real.py       # integração PySAT
│   └── tseitin.py           # Tseitin e DIMACS
├── tests/
├── logicdrive.py            # protótipo Tkinter
├── logicdrive_premium.py    # interface principal
├── main.py                  # demonstração no terminal
└── README.md
```

## Integrantes

- Yan
- Felipe
- Vinicius

## Ferramentas

Python, CustomTkinter, Pillow, pytest, PySAT, Git e GitHub. Ferramentas de IA foram utilizadas como apoio ao desenvolvimento e à documentação.
