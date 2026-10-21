import random
import copy
import pygad

from lerBrasil58  import distancias, custoCaminho, inicializaPopulacao, calculaAptidao


QTDE_CIDADES = 58          # Instância brasil58
TAMANHO_POPULACAO = 200    # Quantidade de indivíduos por geração
GERACOES = 1000            # Número máximo de gerações
TAXA_CROSSOVER = 0.85      # 85% de chance de ocorrer cruzamento
TAXA_MUTACAO = 0.20        # 20% de chance de um filho sofrer mutação
TAMANHO_TORNEIO = 5        # Quantidade de participantes no torneio de seleção


def fitness_func(ga_instance, solution, solution_idx):
    """ 

    Calcula a aptidão de uma solução (caminho) com base no custo total do caminho.
    Define o quão bom é o caminho em termos de distância percorrida.
    Quanto menor o custo, maior a aptidão.

    """
    custo = custoCaminho(solution, distancias)
    return 1.0 / (custo + 1e-6) # o 1e-6 é para evitar divisão por zero, caso o custo seja zero.


def crossover_func(parents, num_children, ga_instance):

    index1 = random.randint(0, QTDE_CIDADES - 1)
    index2 = random.randint(0, QTDE_CIDADES - 1)

    index1, index2 = min(index1, index2), max(index1, index2)

    children = []
    while num_children > 0:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        child = parent1[:index1] + [city for city in parent2[index1:index2] if city not in parent1[:index1]] + parent1[index2:]
        children.append(child)

        num_children -= 1
    
    return children

def swap():
    return
    

def executar_ag():
    '''  

    Executa o algoritmo genérico
    
    '''
    
    populacao = inicializaPopulacao(TAMANHO_POPULACAO, QTDE_CIDADES)


    ga_instance = pygad.GA(
        num_generations=GERACOES,
        fitness_func=fitness_func,
        crossover_type=crossover_func,
        mutation_probability=TAXA_MUTACAO,
        K_tournament=TAMANHO_TORNEIO,
        gene_type=int,

    )

    ga_instance.run()

    melhor_solucao, melhor_aptidao, _ = ga_instance.best_solution()
    melhor_custo = custoCaminho(melhor_solucao, distancias)

    return melhor_solucao, melhor_custo
