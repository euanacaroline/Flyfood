from itertools import permutations
import time

with open("matriz.txt", "r") as file:
    linhas, colunas = map(int, file.readline().split())
    matriz = file.read().splitlines()

coordenadas = {}
pontos_de_entrega = []

for linha, conteudo in enumerate(matriz):
    elementos = conteudo.split()

    for coluna, ponto in enumerate(elementos):
        if ponto != "0":
            coordenadas[ponto] = (linha, coluna)

            if ponto != "R":
                pontos_de_entrega.append(ponto)

menor_custo = float("inf")
melhor_rota = None

inicio = time.perf_counter()

for permutacao in permutations(pontos_de_entrega):

    rota_atual = ("R",) + permutacao + ("R",)
    custo_atual = 0

    for atual, proximo in zip(rota_atual, rota_atual[1:]):

        linha1, coluna1 = coordenadas[atual]
        linha2, coluna2 = coordenadas[proximo]
        custo_atual += (abs(linha1 - linha2) + abs(coluna1 - coluna2))

    if custo_atual < menor_custo:
        menor_custo = custo_atual
        melhor_rota = rota_atual

fim = time.perf_counter()
tempo_execucao = fim - inicio

print("Melhor rota:", " -> ".join(melhor_rota))
print("Menor custo:", menor_custo)
print(f"Tempo de execução: {tempo_execucao:.6f} segundos")