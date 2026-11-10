# FlyFood: Otimização de Rotas de Entrega Urbanas por Drones

Aplicação de arquitetura meta-heurística híbrida (Algoritmo Genético + Busca Local 2-Opt) para o Problema do Caixeiro Viajante (PCV) em ambiente discreto (FlyFood) e validação de escalabilidade geográfica em grande porte (Brasil58).

## 📌 Sobre o Projeto

O **FlyFood** é um projeto de otimização de rotas para entregas autônomas por drones. O objetivo é determinar o circuito fechado de menor custo que parte de um restaurante/depósito central ($R$), visita cada ponto de entrega exatamente uma vez e retorna à origem.

Devido à classificação do PCV como um problema $NP$-Difícil e ao crescimento fatorial do espaço de busca $O(N!)$, abordagens de busca exaustiva (Força Bruta) tornam-se inviáveis em cenários práticos. Este repositório contém a evolução do sistema para um **Algoritmo Memético**, que combina a exploração populacional do Algoritmo Genético com a intensificação geométrica do 2-Opt.

## 🛠️ Arquitetura Algorítmica

### 1. Algoritmo Genético (AG)
* **Framework:** DEAP (Python)
* **Representação:** Permutação de vértices
* **Função de Aptidão (Fitness):** $Fitness(R) = \frac{1}{\text{Custo}(R)}$
* **Cruzamento:** Order Crossover (OX) com probabilidade de $85\%$
* **Mutação Híbrida:** Inversão de segmento ($15\%$) e Troca simples/Swap ($15\%$)
* **Seleção de Pais:** Torneio ($K=2$)
* **Sobrevivência:** Elitismo estrito ($E=1$) + Amostragem Universal Estocástica ($199$ vagas)

### 2. Busca Local (2-Opt)
* **Mecânica:** Substituição de arestas desconexas e inversão de segmento quando $\Delta C < 0$
* **Gatilho por Estagnação:** Ativado após $1.000$ gerações sem melhora na população
* **Pós-Processamento:** Aplicação final sobre até $100$ rotas arquivadas no *Hall of Fame*

## 📊 Instâncias Testadas

| Instância | Destinos ($N$) | Métrica de Custo | Espaço de Busca | Baseline / Ótimo |
| :--- | :---: | :--- | :---: | :---: |
| **FlyFood** | 13 entregas + 1 depot | Distância de Manhattan (Grid) | $13! \approx 6,22 \times 10^9$ | **40 dronômetros** |
| **Brasil58** | 58 cidades | Matriz Simétrica (TSPLIB) | $\frac{57!}{2} \approx 2,03 \times 10^{16}$ | **25.395 unidades** |

## 📈 Resultados Obtidos (30 Sementes Estocásticas)

* **FlyFood (13 entregas):** Atingiu o ótimo global de **40 dronômetros em 29 de 30 execuções** (acurácia de $96,6\%$).
* **Brasil58 (58 cidades):** Custo mediano de **26.007** e menor custo de **25.482** (desvio de apenas $0,34\%$ do ótimo publicado).

## 🚀 Como Executar

### Pré-requisitos
* Python 3.10+
* Biblioteca DEAP

```bash
pip install deap
