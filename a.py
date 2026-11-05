import random
from time import time

from deap import algorithms, base, creator, tools

from lerBrasil58 import distancias
from lerFlyfood import distancias_flyfood, ponto_inicio, pontos_entrega

TAMANHO_POPULACAO, GERACOES = 200, 5000
TAXA_CROSSOVER, TAXA_MUTACAO = 0.85, 0.12
NUMERO_PAIS_REPRODUZINDO, TAMANHO_TORNEIO = 100, 2
ELITISMO = 1  # melhores mantidos sempre; o restante da próxima geração vem da SSS  # 2-Opt dentro da evolução
LIMITE_ESTAGNACAO = 1500  # gerações sem melhora para encerrar (0 desativa)
TAMANHO_HALL = 10  # candidatos refinados com 2-Opt ao final
INTERVALO_LOG = 100

PROBLEMAS = {
    "1": {"nome": "BRASIL58", "genes": list(range(1, 59)), "inicio": None, "distancias": distancias},
    "2": {"nome": "FLYFOOD", "genes": list(pontos_entrega), "inicio": ponto_inicio, "distancias": distancias_flyfood},
}

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # fitness = 1 / custo
creator.create("Individual", list, fitness=creator.FitnessMax)


def custo_tour(tour, matriz):
    """Custo do circuito fechado sobre índices de nós."""
    return sum(matriz[a][b] for a, b in zip(tour, tour[1:] + tour[:1]))


def algoritmo_2opt(tour, matriz):
    """2-Opt (primeira melhoria) com a posição 0 fixa; no Brasil58 isso não restringe a vizinhança."""
    tour, n, melhorou = list(tour), len(tour), True
    while melhorou:
        melhorou = False
        for i in range(1, n - 1):
            a, b = tour[i - 1], tour[i]
            for j in range(i + 1, n):
                c, e = tour[j], tour[(j + 1) % n]
                if matriz[a][c] + matriz[b][e] < matriz[a][b] + matriz[c][e]:
                    tour[i:j + 1] = tour[i:j + 1][::-1]
                    melhorou, b = True, tour[i]
    return tour


def executar_ag(cfg):
    genes, inicio, dic = cfg["genes"], cfg["inicio"], cfg["distancias"]
    n, desloc = len(genes), int(inicio is not None)
    nos = ([inicio] if desloc else []) + genes  # no FlyFood o início é o nó 0, fixo na rota
    matriz = [[dic.get((a, b), 0) for b in nos] for a in nos]
    para_tour = lambda ind: list(range(desloc)) + [g + desloc for g in ind]

    def mutacao(ind):  # o varAnd invalida o fitness; a reavaliação acontece em avaliar()
        if random.random() < TAXA_MUTACAO:
            tools.mutInversion(ind)
        if random.random() < TAXA_MUTACAO:
            tools.mutShuffleIndexes(ind, 1 / n)  # ~1 troca por aplicação
        return (ind,)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(n), n)  # permutação (exigido pelo cxOrdered)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda ind: (1 / custo_tour(para_tour(ind), matriz),))
    toolbox.register("clone", creator.Individual)  # cópia rápida (fitness começa inválido)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", mutacao)
    toolbox.register("select_parents", tools.selTournament, tournsize=TAMANHO_TORNEIO)
    toolbox.register("select_survivors", lambda pool, k: tools.selBest(pool, ELITISMO)
                     + tools.selStochasticUniversalSampling(pool, k - ELITISMO))

    def avaliar(individuos):
        invalidos = [i for i in individuos if not i.fitness.valid]
        for ind, fit in zip(invalidos, map(toolbox.evaluate, invalidos)):
            ind.fitness.values = fit

    populacao = toolbox.population(n=TAMANHO_POPULACAO)
    avaliar(populacao)

    hall = tools.HallOfFame(TAMANHO_HALL)  # guarda os melhores já vistos
    hall.update(populacao)
    melhor_fit, sem_melhora = hall[0].fitness.values[0], 0

    for geracao in range(1, GERACOES + 1):
        pais = toolbox.select_parents(populacao, NUMERO_PAIS_REPRODUZINDO)
        descendentes = algorithms.varAnd(random.choices(pais, k=TAMANHO_POPULACAO), toolbox, TAXA_CROSSOVER, 1.0)
        avaliar(descendentes)
        hall.update(descendentes)
        populacao = toolbox.select_survivors(populacao + descendentes, TAMANHO_POPULACAO)

        fit_atual = hall[0].fitness.values[0]  # o hall nunca piora
        sem_melhora = 0 if fit_atual > melhor_fit else sem_melhora + 1
        melhor_fit = fit_atual
        if geracao % INTERVALO_LOG == 0:
            print(f"Geração {geracao:5d} | melhor custo: {1 / melhor_fit:.0f}")
        if LIMITE_ESTAGNACAO and sem_melhora >= LIMITE_ESTAGNACAO:
            print(f"Parada por estagnação na geração {geracao}.")
            break

    melhor_tour = min((algoritmo_2opt(para_tour(ind), matriz) for ind in hall), key=lambda t: custo_tour(t, matriz))
    return ([genes[i] for i in hall[0]], 1 / hall[0].fitness.values[0],
            [nos[v] for v in melhor_tour[desloc:]], custo_tour(melhor_tour, matriz))


def exibir_resultado(cfg, resultado, tempo_total):
    rota_ga, custo_ga, rota_2opt, custo_2opt = resultado
    ini = cfg["inicio"]
    pre, suf = (f"{ini} -> ", f" -> {ini}") if ini else ("", "")
    ganho = (custo_ga - custo_2opt) / custo_ga * 100 if custo_ga else 0
    print("=" * 120, f"RESULTADO COMPARATIVO - {cfg['nome']}".center(120), "=" * 120,
          f"Quantidade de cidades/pontos: {len(cfg['genes'])}",
          f"1. Custo de saída do AG (memético) : {custo_ga:.2f}",
          f"2. Custo final (2-Opt nos {TAMANHO_HALL} melhores): {custo_2opt:.2f}",
          f"   -> Redução de custo no refino final: {ganho:.2f}%", "-" * 120,
          f"Rota do AG:\n{pre}{' -> '.join(map(str, rota_ga))}{suf}",
          f"Rota final:\n{pre}{' -> '.join(map(str, rota_2opt))}{suf}",
          f"Tempo total de execução: {tempo_total:.2f} segundos", "=" * 120, sep="\n")


if __name__ == "__main__":
    opcao = ""
    while opcao not in PROBLEMAS:
        opcao = input("\nEscolha o problema (1 - Brasil58, 2 - FlyFood): ").strip()
    cfg = PROBLEMAS[opcao]
    inicio = time()
    exibir_resultado(cfg, executar_ag(cfg), time() - inicio)