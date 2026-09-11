from itertools import permutations
file = open("matriz.txt", "r")
i, j = file.readline().split() 
linhas = file.read().splitlines() 

coordenadas = {}
pontos_de_entrega = []