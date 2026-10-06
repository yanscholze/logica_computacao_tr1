# Diagnóstico Lógico de Partida de um Veículo

Projeto desenvolvido para a disciplina de **Lógica para Computação**.

A ideia do projeto é desenvolver um sistema de **diagnóstico lógico de partida de um veículo**, utilizando conceitos de lógica proposicional para representar as condições necessárias para o funcionamento do motor.

O programa será desenvolvido em **Python** e utilizará fórmulas lógicas para representar e avaliar diferentes situações do sistema de partida.

## Variáveis

Inicialmente, utilizaremos as seguintes variáveis proposicionais:

- **B** = bateria possui tensão adequada
- **M** = motor de partida gira
- **C** = combustível disponível
- **I** = sistema de ignição funciona
- **E** = ECU permite a partida
- **P** = motor entra em funcionamento

Cada variável poderá assumir o valor **Verdadeiro (V)** ou **Falso (F)**.

## Regras iniciais

Algumas das regras utilizadas pelo sistema serão:

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

representa:

> Se o motor de partida gira, existe combustível, o sistema de ignição funciona e a ECU permite a partida, então o motor entra em funcionamento.

## Objetivos

Durante o desenvolvimento, o projeto deverá ser capaz de:

- Representar fórmulas de lógica proposicional;
- Avaliar fórmulas a partir dos valores das variáveis;
- Buscar combinações que satisfaçam as regras;
- Identificar situações satisfatíveis e insatisfatíveis;
- Converter fórmulas para a Forma Normal Conjuntiva (FNC);
- Aplicar esses conceitos ao diagnóstico de partida do veículo;
- Realizar testes automatizados das principais funcionalidades.

## Tecnologias

- **Python**
- **Git**
- **GitHub**

## Status

🚧 Projeto em desenvolvimento.

Atualmente estamos definindo a modelagem lógica e iniciando a implementação da estrutura utilizada para representar as fórmulas.