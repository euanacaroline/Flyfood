import os 
import random 

def carregar_matriz_flyfood(nome_arq="matriz.txt"):
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(diretorio, nome_arq) 

    with open(caminho, "r") as arq: 
        linhas = arq.readlines()

    matriz = [linha.split() for linha in linhas if linha.strip()]
    if len(matriz[0]) == 2 and matriz[0][0].isdigit() and matriz[0][1].isdigit():
        matriz = matriz[1:]

    pontos = {}
    for i, linha in enumerate(matriz): 
        for j, valor in enumerate(linha): 
            if valor != "0" and valor.isupper(): 
                pontos[valor] = (i, j)


    distancias = {}
    for p1, (x1, y1) in pontos.items():
        for p2, (x2, y2) in pontos.items():
            if p1 != p2:
                distancias[(p1, p2)] = abs(x1 - x2) + abs(y1 - y2)

    lista_pontos = [p for p in pontos.keys() if p != 'R']


    return distancias, lista_pontos, 'R'

def custoCaminhoFlyfood(rota, dic_distancias, ponto_r='R'):
    rota_completa = [ponto_r] + list(rota) + [ponto_r]
    custo = 0
    for i in range(len(rota_completa) - 1):
        u, v = rota_completa[i], rota_completa[i + 1]
        custo += dic_distancias[(u, v)]
    return custo

def inicializaPopulacaoFlyfood(tamanho_pop, lista_pontos):
    populacao = []
    for _ in range(tamanho_pop):
        individuo = list(lista_pontos)
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao

distancias_flyfood, pontos_entrega, ponto_inicio = carregar_matriz_flyfood("matriz.txt")