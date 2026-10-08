# Diagnóstico Lógico de Partida de um Veículo

Projeto desenvolvido para a disciplina de **Lógica para Computação**.

O sistema utiliza lógica proposicional para representar e analisar as condições envolvidas na partida de um veículo, integrando representação de fórmulas, avaliação de valorações, busca de modelos, SAT e conversão para Forma Normal Conjuntiva (FNC).

---

## Contexto

O projeto representa algumas condições básicas envolvidas no funcionamento de um veículo por meio de variáveis proposicionais.

### Variáveis

| Variável | Significado |
|----------|-------------|
| `B` | Bateria possui tensão adequada |
| `M` | Motor de partida gira |
| `C` | Combustível disponível |
| `I` | Sistema de ignição funciona |
| `E` | ECU permite a partida |
| `P` | Motor entra em funcionamento |

Cada variável pode assumir os valores `True` ou `False`.

---

## Regras do sistema

O diagnóstico utiliza as seguintes restrições:

```text
(B ∧ E) → M
(M ∧ C ∧ I ∧ E) → P
P → M
P → C
P → I
```

Por exemplo:

```text
(M ∧ C ∧ I ∧ E) → P
```

significa:

> Se o motor de partida gira, existe combustível, o sistema de ignição funciona e a ECU permite a partida, então o motor entra em funcionamento.

Todas as regras são reunidas em uma única fórmula lógica, permitindo analisar o sistema completo.

---

## Funcionalidades

O projeto implementa:

- representação de fórmulas através de uma Árvore Sintática Abstrata (AST);
- operadores `¬`, `∧`, `∨`, `→` e `↔`;
- impressão de fórmulas em notação infixa;
- avaliação de fórmulas para uma determinada valoração;
- identificação das variáveis de uma fórmula;
- cálculo do tamanho da AST;
- busca exaustiva de modelos;
- identificação de satisfatibilidade;
- contagem de modelos;
- classificação como válida, contingente ou insatisfatível;
- conversão clássica para Forma Normal Conjuntiva (FNC);
- geração da lista de cláusulas da FNC;
- diagnóstico aplicado ao contexto automotivo;
- variante propositalmente insatisfatível;
- testes automatizados;
- verificação da equivalência entre a fórmula original e sua FNC por tabela-verdade.

---

## Estrutura

```text
logica_computacao_tr1/
│
├── src/
│   ├── __init__.py
│   ├── formula.py
│   ├── r3_solver.py
│   ├── r4_cnf.py
│   └── diagnostico.py
│
├── tests/
│   ├── test_formula.py
│   ├── test_r3_solver.py
│   ├── test_r4_cnf.py
│   ├── test_diagnostico.py
│   └── test_r6.py
│
├── main.py
├── README.md
└── .gitignore
```

---

## Execução

### Requisitos

- Python 3
- pytest

Instale o pytest, caso necessário:

```bash
python -m pip install pytest
```

Execute a demonstração:

```bash
python main.py
```

Execute todos os testes:

```bash
python -m pytest
```

Para visualizar cada teste individualmente:

```bash
python -m pytest -v
```

---

## Representação das fórmulas

As fórmulas são representadas através de objetos que formam uma AST.

Exemplo:

```python
P = Variable("P")
Q = Variable("Q")

formula = Implies(P, Q)
```

Representa:

```text
P → Q
```

Internamente:

```text
    →
   / \
  P   Q
```

A avaliação percorre essa árvore recursivamente.

---

## Busca de modelos e SAT

Para uma fórmula com `n` variáveis existem:

```text
2^n
```

valorações possíveis.

O projeto percorre essas combinações e identifica quais tornam a fórmula verdadeira.

Com isso, uma fórmula pode ser classificada como:

- **válida** — verdadeira em todas as valorações;
- **contingente** — verdadeira apenas em algumas valorações;
- **insatisfatível** — falsa em todas as valorações.

---

## Forma Normal Conjuntiva

A conversão para FNC é realizada em três etapas principais:

1. eliminação de `→` e `↔`;
2. transformação para Forma Normal da Negação (FNN);
3. distribuição de `∨` sobre `∧`.

Exemplo:

```text
P → Q
```

torna-se:

```text
¬P ∨ Q
```

A FNC também pode ser exportada como uma lista de cláusulas.

---

## Variante insatisfatível

Para demonstrar um caso sem modelos, o projeto utiliza:

```text
SISTEMA ∧ P ∧ ¬M
```

Como uma das regras do sistema estabelece:

```text
P → M
```

não existe uma valoração capaz de satisfazer simultaneamente `P` e `¬M`.

Logo, essa variante é **insatisfatível (UNSAT)**.

---

## Testes

Os testes automatizados verificam, entre outros casos:

- avaliação das fórmulas;
- busca e contagem de modelos;
- tautologia;
- contradição;
- fórmula contingente;
- eliminação de implicações;
- Leis de De Morgan;
- distribuição para FNC;
- geração de cláusulas;
- diagnóstico automotivo;
- equivalência entre a fórmula original e a FNC por tabela-verdade.

Execute:

```bash
python -m pytest -v
```

---
## Interface gráfica — LogicDrive

A interface gráfica do projeto está disponível na branch `felipe-ui-premium` e utiliza **CustomTkinter**.

Ela permite selecionar diferentes cenários automotivos e visualizar o diagnóstico do veículo de forma interativa. A interface utiliza a lógica implementada em `src/diagnostico.py` para analisar os estados do sistema.

### Manual de inicialização da UI

#### 1. Clonar o repositório

```bash
git clone https://github.com/yanscholze/logica_computacao_tr1.git
cd logica_computacao_tr1
```

#### 2. Buscar as branches do projeto

```bash
git fetch --all
```

#### 3. Entrar na branch da interface

```bash
git checkout felipe-ui-premium
```

Caso a branch ainda não exista localmente:

```bash
git checkout -b felipe-ui-premium origin/felipe-ui-premium
```

#### 4. Instalar as dependências

```bash
python -m pip install customtkinter pillow pytest python-sat
```

No Linux, caso o comando utilizado seja `python3`:

```bash
python3 -m pip install customtkinter pillow pytest python-sat
```

As principais dependências são:

- `customtkinter` — componentes da interface gráfica;
- `Pillow` — carregamento da imagem do veículo;
- `pytest` — execução dos testes automatizados;
- `python-sat` — integração com o SAT Solver PySAT.

#### 5. Iniciar a interface

```bash
python logicdrive_premium.py
```

No Linux:

```bash
python3 logicdrive_premium.py
```

### Inicialização rápida

Para uma máquina que já possui Git e Python instalados:

```bash
git clone https://github.com/yanscholze/logica_computacao_tr1.git
cd logica_computacao_tr1
git fetch --all
git checkout felipe-ui-premium
python -m pip install customtkinter pillow pytest python-sat
python logicdrive_premium.py
```

O arquivo principal da interface atual é:

```text
logicdrive_premium.py
```

O arquivo `logicdrive.py` corresponde ao protótipo inicial da interface desenvolvido com Tkinter.

## Integrantes

- **Yan**
- **Felipe**
- **Vinicius**

---

## Divisão das atividades

| Integrante | Responsabilidade |
|------------|------------------|
| Yan | Estrutura dos Dados, Impressão e avaliação (R1 e R2) |
| Yan | Aplicação do diagnóstico automotivo, integração e testes (R5 e R6) |
| Felipe | Busca de modelos e classificação SAT (R3) |
| Felipe | Conversão para Forma Normal Conjuntiva (R4) |
| Yan | Implementação dos Extras |
| Yan e Felipe | Implementaçã oda UI/UX |
| Grupo | Modelagem, testes, documentação e apresentação |


---
## Ferramentas utilizadas

- Python
- pytest
- Git
- GitHub
- ChatGPT
- Codex

Ferramentas de inteligência artificial foram utilizadas como apoio durante o desenvolvimento, revisão, organização e compreensão do código.

---

## Status

**R1 a R6 implementados e testados.**

**Extras implementados: parser, DPLL, Tseitin/DIMACS e integração com PySAT.**

**Interface gráfica LogicDrive implementada na branch `felipe-ui-premium`.**