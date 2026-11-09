import random
from time import time
from deap import algorithms, base, creator, tools
from lerBrasil58 import distancias
from lerFlyfood import distancias_flyfood, ponto_inicio, pontos_entrega

TAMANHO_POPULACAO = 200
NUMERO_GERACOES = 5000
TAXA_CROSSOVER = 0.85 
TAXA_MUTACAO = 0.15
NUMERO_PAIS_REPRODUZINDO = 100
TAMANHO_TORNEIO = 2
ELITISMO = 1
LIMITE_ESTAGNACAO = 3000
INTERVALO_2OPT = 1000
QUANTIDADE_2OPT = 10
TAMANHO_LISTA_MELHORES = 100
INTERVALO_REGISTRO = 100
PROBLEMAS = {
    "1": {
        "nome":"BRASIL58",
        "genes": list(range(1, 59)),
        "inicio": None,
        "distancias": distancias
    },
    
    "2": {
        "nome": "FLYFOOD",
        "genes": list(pontos_entrega),
        "inicio": ponto_inicio,
        "distancias": distancias_flyfood
    },
}

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def custo_tour(rota, matriz):
    """Custo do circuito fechado sobre índices de nós."""
    return sum(matriz[no_atual][proximo_no] for no_atual, proximo_no in zip(rota, rota[1:] + rota[:1]))

def algoritmo_2opt(rota, matriz):
    """Algoritmo 2-opt para refinar os 10 melhores candidatos do hall."""
    rota = list(rota)
    quantidade_nos = len(rota)
    houve_melhoria = True
    while houve_melhoria:
        houve_melhoria = False
        for indice_inicio in range(1, quantidade_nos - 1):
            no_anterior, no_atual = rota[indice_inicio - 1], rota[indice_inicio]
            for indice_fim in range(indice_inicio + 1, quantidade_nos):
                proximo_no, no_final = rota[indice_fim], rota[(indice_fim + 1) % quantidade_nos]
                if matriz[no_anterior][proximo_no] + matriz[no_atual][no_final] < matriz[no_anterior][no_atual] + matriz[proximo_no][no_final]:
                    rota[indice_inicio:indice_fim + 1] = rota[indice_inicio:indice_fim + 1][::-1]
                    houve_melhoria, no_atual = True, rota[indice_inicio]

    return rota

def executar_ag(configuracao):
    """Execução do algoritmo genético ao problema definido em `configuracao`."""
    lista_genes = configuracao["genes"]
    ponto_inicio = configuracao["inicio"]
    mapa_distancias = configuracao["distancias"]
    
    quantidade_genes = len(lista_genes)
    deslocamento = int(ponto_inicio is not None)
    lista_nos = ([ponto_inicio] if deslocamento else []) + lista_genes
    matriz_distancias = [[mapa_distancias.get((no_origem, no_destino), 0) for no_destino in lista_nos] for no_origem in lista_nos]
    converter_individuo_para_rota = lambda individuo: list(range(deslocamento)) + [gene + deslocamento for gene in individuo]

    def mutacao(individuo):
        if random.random() < TAXA_MUTACAO:
            tools.mutInversion(individuo)
            
        if random.random() < TAXA_MUTACAO:
            tools.mutShuffleIndexes(individuo, 1 / quantidade_genes)  

        return (individuo,)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(quantidade_genes), quantidade_genes)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda individuo: (1 / custo_tour(converter_individuo_para_rota(individuo), matriz_distancias),))
    toolbox.register("clone", creator.Individual)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", mutacao)
    toolbox.register("select_parents", tools.selTournament, tournsize=TAMANHO_TORNEIO)
    toolbox.register("select_survivors", lambda populacao_candidata, tamanho_populacao: tools.selBest(populacao_candidata, ELITISMO) + tools.selStochasticUniversalSampling(populacao_candidata, tamanho_populacao - ELITISMO))

    def avaliar(lista_individuos):
        """Avalia a aptidão de indivíduos inválidos."""
        individuos_invalidos = [individuo for individuo in lista_individuos if not individuo.fitness.valid]
        for individuo, aptidao in zip(individuos_invalidos, map(toolbox.evaluate, individuos_invalidos)):
            individuo.fitness.values = aptidao

    def refinar_populacao(populacao):
        """Aplica 2-opt em indivíduos aleatórios da população."""
        individuos_selecionados = random.sample(populacao, min(QUANTIDADE_2OPT, len(populacao)))
        individuos_refinados = []
        for individuo in individuos_selecionados:
            rota = converter_individuo_para_rota(individuo)
            rota_refinada = algoritmo_2opt(rota, matriz_distancias)
            genes_refinados = [no - deslocamento for no in rota_refinada[deslocamento:]]
            individuo_refinado = creator.Individual(genes_refinados)
            individuos_refinados.append(individuo_refinado)

        avaliar(individuos_refinados)
        return individuos_refinados

    populacao = toolbox.population(n=TAMANHO_POPULACAO)
    avaliar(populacao)
    melhores_individuos = tools.HallOfFame(TAMANHO_LISTA_MELHORES)
    melhores_individuos.update(populacao)
    melhor_aptidao, geracoes_sem_melhoria = melhores_individuos[0].fitness.values[0], 0
    proxima_ativacao_2opt = INTERVALO_2OPT

    for geracao in range(1, NUMERO_GERACOES + 1):
        pais = toolbox.select_parents(populacao, NUMERO_PAIS_REPRODUZINDO)
        descendentes = algorithms.varAnd(random.choices(pais, k=TAMANHO_POPULACAO), toolbox, TAXA_CROSSOVER, 1.0)
        avaliar(descendentes)
        melhores_individuos.update(descendentes)
        populacao = toolbox.select_survivors(populacao + descendentes, TAMANHO_POPULACAO)
        aptidao_atual = melhores_individuos[0].fitness.values[0]
        if aptidao_atual > melhor_aptidao:
            melhor_aptidao = aptidao_atual
            geracoes_sem_melhoria = 0
            proxima_ativacao_2opt = INTERVALO_2OPT

        else:
            geracoes_sem_melhoria += 1

        if geracoes_sem_melhoria >= proxima_ativacao_2opt:
            print(f"Estagnação de {geracoes_sem_melhoria} gerações. | Aplicando 2-opt em {QUANTIDADE_2OPT} indivíduos...")
            individuos_refinados = refinar_populacao(populacao)
            melhores_individuos.update(individuos_refinados)
            populacao = toolbox.select_survivors(populacao + individuos_refinados, TAMANHO_POPULACAO)
            aptidao_atual = melhores_individuos[0].fitness.values[0]

            if aptidao_atual > melhor_aptidao:
                melhor_aptidao = aptidao_atual
                geracoes_sem_melhoria = 0
                proxima_ativacao_2opt = INTERVALO_2OPT

            else:
                proxima_ativacao_2opt += INTERVALO_2OPT

        if geracao % INTERVALO_REGISTRO == 0:
            print(f"Geração {geracao:5d} | Melhor custo: {1 / melhor_aptidao:.0f} | Estagnação: {geracoes_sem_melhoria}")

        if geracoes_sem_melhoria >= LIMITE_ESTAGNACAO:
            print(f"\nParada por estagnação na geração {geracao}.")
            break

    melhor_rota = min((algoritmo_2opt(converter_individuo_para_rota(individuo), matriz_distancias) for individuo in melhores_individuos), key=lambda rota: custo_tour(rota, matriz_distancias))
    return ([lista_genes[indice_gene] for indice_gene in melhores_individuos[0]], 1 / melhores_individuos[0].fitness.values[0],
        [lista_nos[indice_no] for indice_no in melhor_rota[deslocamento:]], custo_tour(melhor_rota, matriz_distancias))

def exibir_resultado(configuracao, resultado, tempo_total):
    """Exibe o resultado do algoritmo genético e do refinamento 2-opt."""
    rota_algoritmo_genetico, custo_algoritmo_genetico, rota_refinada, custo_refinado = resultado
    ponto_inicio = configuracao["inicio"]
    prefixo, sufixo = (f"{ponto_inicio} -> ", f" -> {ponto_inicio}") if ponto_inicio else ("", "")
    ganho = (custo_algoritmo_genetico - custo_refinado) / custo_algoritmo_genetico * 100 if custo_algoritmo_genetico else 0
    print("=" * 120, f"RESULTADO COMPARATIVO - {configuracao['nome']}".center(120), "=" * 120,
          f"Quantidade de cidades/pontos: {len(configuracao['genes'])}",
          f"1. Custo de saída do AG (memético) : {custo_algoritmo_genetico:.2f}",
          f"2. Custo final (2-Opt nos {TAMANHO_LISTA_MELHORES} melhores): {custo_refinado:.2f}",
          f"   -> Redução de custo no refino final: {ganho:.2f}%", "-" * 120,
          f"Rota do AG:\n{prefixo}{' -> '.join(map(str, rota_algoritmo_genetico))}{sufixo}",
          f"Rota final:\n{prefixo}{' -> '.join(map(str, rota_refinada))}{sufixo}",
          f"Tempo total de execução: {tempo_total:.2f} segundos", "=" * 120, sep="\n")

if __name__ == "__main__":
    opcao = ""
    while opcao not in PROBLEMAS:
        opcao = input("\nEscolha o problema (1 - Brasil58, 2 - FlyFood): ").strip()
        
    configuracao = PROBLEMAS[opcao]
    inicio = time()
    exibir_resultado(configuracao, executar_ag(configuracao), time() - inicio)