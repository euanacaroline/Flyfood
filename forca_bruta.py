from itertools import permutations
file = open("matriz.txt", "r")
i, j = file.readline().split() 
linhas = file.read().splitlines() 

coordenadas = {}
pontos_de_entrega = []

for n in range(int(i)):
    line = linhas[n].split()
    for m in line:
        if m != "0":
            coordenadas[m] = (n, line.index(m))
            pontos_de_entrega.append(m)

pontos_de_entrega.remove("R")
menor_custo = float("inf")

for poss in list(permutations(pontos_de_entrega)): 
    custo_atual = 0 
    indice_rota = 0 
    poss = list(poss)  
    poss.append("R") 
    poss.insert(0, "R") 
    