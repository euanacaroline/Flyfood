# Flyfood

Otimização de Rotas de Entrega com Drones

Este projeto foi desenvolvido como parte da avaliação da disciplina de **Projeto Interdisciplinar de Sistemas de Informação 2** do curso de Bacharelado em Sistemas de Informação da **UFRPE** (Universidade Federal Rural de Pernambuco).

O objetivo do projeto é resolver o problema de roteamento de entregas de um drone em um mapa urbano discretizado em matriz, utilizando uma abordagem de **Força Bruta** baseada no clássico **Problema do Caixeiro Viajante (PCV / TSP)**.

---

## 📌 Sobre o Projeto

A ideia do FlyFood é simples: o drone sai de um ponto de origem (o restaurante `'R'`), precisa visitar todos os pontos de entrega (`'A'`, `'B'`, `'C'`...) exatamente uma vez e retornar ao restaurante pelo menor caminho possível.

Como o drone se desloca em uma grade celular (apenas nas direções vertical e horizontal, sem trajetórias diagonais), utilizamos a **Distância de Manhattan** para calcular o custo do percurso em *dronômetros*.

### Por que usar Força Bruta? 🤔
Apesar de sabermos que a Força Bruta possui complexidade assintótica $O(N! \cdot N)$ e sofre com a explosão combinatória, a escolha dessa estratégia foi proposital para:
1. **Garantir a solução 100% ótima** (servindo como nossa linha de base/*baseline*);
2. **Mapear a pior rota possível** (para entender o limite máximo de consumo de energia da bateria);
3. **Comprovar empiricamente** os limites computacionais do algoritmo conforme o número de entregas $N$ aumenta.

---

## 🛠️ Como o Código Funciona

O script foi desenvolvido em **Python 3** utilizando apenas recursos e bibliotecas nativas da linguagem:

1. **Leitura da Matriz (`matriz.txt`):** O código lê o arquivo de entrada e usa `enumerate()` para mapear os caracteres em coordenadas cartesianas $(y, x)$, separando a origem `'R'` dos destinos de entrega.
2. **Geração de Permutações:** Utiliza o módulo `itertools.permutations` para gerar todas as $N!$ ordens possíveis de visitação.
3. **Cálculo da Rota Fechada:** Encadeia a origem `'R'` no início e no fim da rota e calcula a distância acumulada entre pares vizinhos via `zip()` e `abs()`.
4. **Rastreamento de Extremos:** Compara e armazena continuamente a **melhor rota** ($C_{\min}$) e a **pior rota** ($C_{\max}$).
5. **Métricas de Desempenho:** Cronometra o tempo de processamento com `time.perf_counter()` e valida o total teórico de possibilidades via função recursiva do fatorial $N!$.

---

## 📂 Estrutura do Arquivo `matriz.txt`

O arquivo de entrada deve estar na mesma pasta do script e seguir o formato abaixo:
- **1ª linha:** Dimensões da matriz (quantidade de linhas e colunas).
- **Linhas seguintes:** A representação visual do mapa.
  - `'R'`: Restaurante (ponto de partida e chegada).
  - `'0'`: Espaço aéreo livre.
  - `'A'`, `'B'`, `'C'`...: Pontos de entrega.

**Exemplo:**
```text
4 5
R 0 0 0 A
0 0 B 0 0
0 0 0 0 0
0 C 0 0 0
