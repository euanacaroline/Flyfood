import random
import numpy as np
import pygad
from lerBrasil58 import custoCaminho, distancias, inicializaPopulacao

QTDE_CIDADES = 58
TAMANHO_POPULACAO = 250
GERACOES = 5000
TAXA_CROSSOVER = 0.85
TAXA_MUTACAO = 0.20
NUMERO_PAIS = 140
TAMANHO_TORNEIO = 2

def fitness_func(ga_instance, solution, solution_idx):
    """Fitness invertido (quanto menor o custo, maior a aptidão/fitness)."""
    custo = custoCaminho(solution, distancias)
    return 1.0 / 1e-6 if custo == 0 else 1.0 / custo

def crossover_func(parents, offspring_size, ga_instance):
    """Cruzamento Order Crossover (OX) para cromossomos de permutação."""
    num_children, num_genes = offspring_size
    children = []
    num_parents = len(parents)

    for i in range(num_children):
        p1 = list(parents[i % num_parents])
        p2 = list(parents[(i + 1) % num_parents])
        inicio, fim = sorted(random.sample(range(num_genes), 2))
        child = [None] * num_genes
        child[inicio:fim] = p1[inicio:fim]

        cidades_restantes = [
            cidade for cidade in p2 if cidade not in child[inicio:fim]
        ]
        posicoes_restantes = (
            list(range(fim, num_genes)) + list(range(0, inicio))
        )
        for posicao, cidade in zip(posicoes_restantes, cidades_restantes):
            child[posicao] = cidade
        children.append(child)

    return np.array(children, dtype=int)


def mutation_func(offspring, ga_instance):
    """
    Realiza uma mutação híbrida, aplicando a inversão de sub-rota seguida de swap (troca local) para aumentar a variabilidade genética.
    """
    for individuo in offspring:
        if random.random() < TAXA_MUTACAO:
            inicio, fim = sorted(random.sample(range(QTDE_CIDADES), 2))
            individuo[inicio:fim] = individuo[inicio:fim][::-1]

        if random.random() < TAXA_MUTACAO:
            idx1, idx2 = random.sample(range(QTDE_CIDADES), 2)
            individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]

    return offspring


def algoritmo_2opt(rota, dic_distancias):
    """Busca Local 2-Opt através da troca de arestas."""
    melhor_rota = [int(c) for c in rota]
    n = len(melhor_rota)
    melhorou = True

    while melhorou:
        melhorou = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                u1, v1 = melhor_rota[i - 1], melhor_rota[i]
                u2, v2 = melhor_rota[j - 1], melhor_rota[j % n]
                custo_atual = dic_distancias[(u1, v1)] + dic_distancias[(u2, v2)]
                custo_novo = dic_distancias[(u1, u2)] + dic_distancias[(v1, v2)]
                if custo_novo < custo_atual:
                    melhor_rota[i:j] = melhor_rota[i:j][::-1]
                    melhorou = True
                    break

            if melhorou:
                break

    return melhor_rota

def executar_ag():
    populacao_inicial = inicializaPopulacao(TAMANHO_POPULACAO, QTDE_CIDADES)
    ga_instance = pygad.GA(
        num_generations=GERACOES,
        num_parents_mating=NUMERO_PAIS,
        initial_population=populacao_inicial,
        fitness_func=fitness_func,
        crossover_type=crossover_func,
        crossover_probability=TAXA_CROSSOVER,
        mutation_type=mutation_func,
        parent_selection_type="tournament",
        K_tournament=TAMANHO_TORNEIO,
        gene_type=int,
        gene_space=list(range(1, QTDE_CIDADES + 1)),
        allow_duplicate_genes=False,
        keep_elitism=3,
    )

    ga_instance.run()
    melhor_solucao_ga, _, _ = ga_instance.best_solution()
    rota_ga = [int(x) for x in melhor_solucao_ga]
    custo_ga_puro = custoCaminho(rota_ga, distancias)
    rota_2opt = algoritmo_2opt(rota_ga, distancias)
    custo_2opt = custoCaminho(rota_2opt, distancias)
    return rota_ga, custo_ga_puro, rota_2opt, custo_2opt

if __name__ == "__main__":
    rota_ga, custo_ga, rota_2opt, custo_2opt = executar_ag()
    print("=" * 65)
    print("           RESULTADO COMPARATIVO - TSP (BRASIL 58)           ")
    print("=" * 65)
    print(f"1. Custo de Saída do PyGAD (ERX Puro)  : {custo_ga:.2f}")
    print(f"2. Custo Final Otimizado (ERX + 2-Opt) : {custo_2opt:.2f}")
    ganho_perc = ((custo_ga - custo_2opt) / custo_ga) * 100
    print(f"   -> Redução de custo obtida pelo 2-Opt: {ganho_perc:.2f}%")
    print("-" * 65)
    print(f"Rota Otimizada Final:\n{' -> '.join(map(str, rota_2opt))}")
    print("=" * 65)