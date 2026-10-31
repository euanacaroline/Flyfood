import random
import pygad
import numpy
from lerBrasil58 import custoCaminho, distancias, inicializaPopulacao
from lerFlyfood import custoCaminhoFlyfood, distancias_flyfood, inicializaPopulacaoFlyfood, ponto_inicio, pontos_entrega

TAMANHO_POPULACAO = 200
GERACOES = 2500
TAXA_CROSSOVER = 0.85
TAXA_MUTACAO = 0.15
NUMERO_PAIS_REPRODUZINDO = 100
TAMANHO_TORNEIO = 2

def _configurar_problema(opcao):
    """Retorna a configuração de genes, custo e população do problema escolhido."""
    if opcao == "1":
        qtde_cidades = 58
        return {
            "nome": "BRASIL58",
            "qtde_cidades": qtde_cidades,
            "distancias": distancias,
            "custo": custoCaminho,
            "populacao": inicializaPopulacao(TAMANHO_POPULACAO, qtde_cidades),
            "gene_space": list(range(1, qtde_cidades + 1)),
            "converter_rota": lambda rota: [int(cidade) for cidade in rota],
        }

    if opcao == "2":
        qtde_cidades = len(pontos_entrega)
        return {
            "nome": "FLYFOOD",
            "qtde_cidades": qtde_cidades,
            "distancias": distancias_flyfood,
            "custo": custoCaminhoFlyfood,
            "populacao": inicializaPopulacaoFlyfood(TAMANHO_POPULACAO, list(range(qtde_cidades))),
            "gene_space": list(range(qtde_cidades)),
            "converter_rota": lambda rota: [pontos_entrega[int(indice)] for indice in rota],
        }

    raise ValueError("Opção inválida. Escolha 1 para Brasil58 ou 2 para FlyFood.")


def _calcular_custo(rota, configuracao):
    rota_convertida = configuracao["converter_rota"](rota)
    if configuracao["nome"] == "FLYFOOD":
        return configuracao["custo"](rota_convertida, configuracao["distancias"], ponto_inicio)
    
    return configuracao["custo"](rota_convertida, configuracao["distancias"])


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
        cidades_restantes = [cidade for cidade in p2 if cidade not in child[inicio:fim]]
        posicoes_restantes = (list(range(fim, num_genes)) + list(range(0, inicio)))
        for posicao, cidade in zip(posicoes_restantes, cidades_restantes):
            child[posicao] = cidade

        children.append(child)

    return numpy.array(children, dtype=int)


def _criar_mutacao(qtde_cidades):
    def mutation_func(offspring, ga_instance):
        for individuo in offspring:
            if random.random() < TAXA_MUTACAO:
                inicio, fim = sorted(random.sample(range(qtde_cidades), 2))
                individuo[inicio:fim] = individuo[inicio:fim][::-1]

            if random.random() < TAXA_MUTACAO:
                indice_1, indice_2 = random.sample(range(qtde_cidades), 2)
                individuo[indice_1], individuo[indice_2] = (
                    individuo[indice_2],
                    individuo[indice_1],
                )

        return offspring

    return mutation_func


def _criar_fitness(configuracao):
    def fitness_func(ga_instance, solution, solution_idx):
        custo = _calcular_custo(solution, configuracao)
        return 1.0 / 1e-6 if custo == 0 else 1.0 / custo

    return fitness_func


def algoritmo_2opt(rota, dic_distancias):
    """Busca local 2-Opt para uma rota com cidades inteiras ou rotuladas."""
    melhor_rota = list(rota)
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


def executar_ag(configuracao):
    """Executa o algoritmo genético para a configuração selecionada."""
    ga_instance = pygad.GA(
        num_generations=GERACOES,
        num_parents_mating=NUMERO_PAIS_REPRODUZINDO,
        initial_population=configuracao["populacao"],
        fitness_func=_criar_fitness(configuracao),
        crossover_type=crossover_func,
        crossover_probability=TAXA_CROSSOVER,
        mutation_type=_criar_mutacao(configuracao["qtde_cidades"]),
        parent_selection_type="tournament",
        K_tournament=TAMANHO_TORNEIO,
        gene_type=int,
        gene_space=configuracao["gene_space"],
        allow_duplicate_genes=False,
        keep_elitism=100,
    )

    ga_instance.run()
    melhor_solucao_ga, _, _ = ga_instance.best_solution()
    rota_ga = configuracao["converter_rota"](melhor_solucao_ga)
    custo_ga = (custoCaminhoFlyfood(rota_ga, distancias_flyfood, ponto_inicio) if configuracao["nome"] == "FLYFOOD" else custoCaminho(rota_ga, distancias))
    rota_2opt = algoritmo_2opt(rota_ga, configuracao["distancias"])
    custo_2opt = (custoCaminhoFlyfood(rota_2opt, distancias_flyfood, ponto_inicio) if configuracao["nome"] == "FLYFOOD" else custoCaminho(rota_2opt, distancias))
    return rota_ga, custo_ga, rota_2opt, custo_2opt

def selecionar_problema():
    while True:
        print("\nEscolha o problema que deseja resolver:")
        print("1 - Brasil58")
        print("2 - FlyFood")
        opcao = input("Digite a opção: ").strip()
        if opcao in {"1", "2"}:
            return opcao
        
        print("Opção inválida. Digite 1 ou 2.")

def exibir_resultado(configuracao, resultado):
    rota_ga, custo_ga, rota_2opt, custo_2opt = resultado
    ganho_perc = ((custo_ga - custo_2opt) / custo_ga) * 100 if custo_ga else 0
    print("=" * 120)
    print(f"           RESULTADO COMPARATIVO - {configuracao['nome']}           ")
    print("=" * 120)
    print(f"Quantidade de cidades/pontos: {configuracao['qtde_cidades']}")
    print(f"1. Custo de saída do AG          : {custo_ga:.2f}")
    print(f"2. Custo final otimizado (2-Opt)    : {custo_2opt:.2f}")
    print(f"   -> Redução de custo pelo 2-Opt: {ganho_perc:.2f}%")
    print("-" * 120)
    print(f"Rota inicial do AG:\n{' -> '.join(map(str, rota_ga))}")
    print(f"Rota otimizada final:\n{' -> '.join(map(str, rota_2opt))}")
    print("=" * 120)

if __name__ == "__main__":
    opcao = selecionar_problema()
    configuracao = _configurar_problema(opcao)
    exibir_resultado(configuracao, executar_ag(configuracao))
