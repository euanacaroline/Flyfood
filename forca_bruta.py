from itertools import permutations
import time

with open("matriz.txt", "r") as file:
    linhas, colunas = map(int, file.readline().split())
    matriz = file.read().splitlines()

coordenadas = {}
pontos_de_entrega = []
inicio = time.perf_counter()

for linha, conteudo in enumerate(matriz):
    elementos = conteudo.split()

    for coluna, ponto in enumerate(elementos):
        if ponto != "0":
            coordenadas[ponto] = (linha, coluna)

            if ponto != "R":
                pontos_de_entrega.append(ponto)

menor_custo = float("inf")
melhor_rota = None
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
horas = int(tempo_execucao // 3600)
minutos = int((tempo_execucao % 3600) // 60)
segundos = tempo_execucao % 60

def calcular_total_possibilidades(cidades: int) -> int:
    if cidades == 1:
        return cidades
    else:
        return cidades * calcular_total_possibilidades(cidades - 1)

qtd_pontos_entregas = len(coordenadas) - 1 
total_possibilidades = calcular_total_possibilidades(qtd_pontos_entregas)

print(f"Total de possibilidades para {qtd_pontos_entregas} pontos de entrega: {total_possibilidades}")
print(f"Melhor rota: {' -> '.join(melhor_rota)}")
print(f"Menor custo: {menor_custo}")
print(f"Tempo de processo: {horas} hora(s), {minutos} minuto(s) e {segundos:.2f} segundo(s)")