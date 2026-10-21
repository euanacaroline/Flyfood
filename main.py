import random
import copy

from lerBrasil58  import distancias, custoCaminho, inicializaPopulacao, calculaAptidao


QTDE_CIDADES = 58          # Instância brasil58
TAMANHO_POPULACAO = 200    # Quantidade de indivíduos por geração
GERACOES = 1000            # Número máximo de gerações
TAXA_CROSSOVER = 0.85      # 85% de chance de ocorrer cruzamento
TAXA_MUTACAO = 0.20        # 20% de chance de um filho sofrer mutação
TAMANHO_TORNEIO = 5        # Quantidade de participantes no torneio de seleção



def executar_ag():
    '''  

    Executa o algoritmo genérico
    
    '''
    populacao = inicializaPopulacao(TAMANHO_POPULACAO, QTDE_CIDADES)
    custo = calculaAptidao(populacao, distancias)


    return populacao, custo



p, c = executar_ag()


print(c)



