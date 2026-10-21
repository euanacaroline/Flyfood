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
    

def executar_ag():
    '''  

    Executa o algoritmo genérico
    
    '''
    populacao = inicializaPopulacao(TAMANHO_POPULACAO, QTDE_CIDADES)


    ag_instance = pygad.GA(
        num_generations=GERACOES,

    )

    

p, c = executar_ag()


print(c)



