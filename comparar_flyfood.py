import time
import itertools
import numpy as np
import pygad
from lerFlyfood import distancias_flyfood, pontos_entrega, ponto_inicio, custoCaminhoFlyfood, inicializaPopulacaoFlyfood

pontos_usados = pontos_entrega[:8]

def forca_bruta_flyfood():
    inicio = time.time()
    melhor_custo = float('inf')
    melhor_rota = None
    avaliacoes = 0


    for perm in itertools.permutations(pontos_usados):
        avaliacoes += 1
        custo = custoCaminhoFlyfood(perm, distancias_flyfood, ponto_inicio)
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_rota = perm

    fim = time.time()
    return melhor_rota, melhor_custo, fim - inicio, avaliacoes


def fitness_func_flyfood(ga_instance, solution, solution_idx):
    rota = [pontos_usados[int(i)] for i in solution]
    custo = custoCaminhoFlyfood(rota, distancias_flyfood, ponto_inicio)
    return 1.0 / (custo + 1e-6)

def executar_ag_flyfood():
    pop_size = 30
    generations = 50
    n = len(pontos_usados)
    populacao_inicial = inicializaPopulacaoFlyfood(pop_size, list(range(n)))

    ga_instance = pygad.GA(
        num_generations=generations,
        num_parents_mating=15,
        initial_population=populacao_inicial,
        fitness_func=fitness_func_flyfood,
        parent_selection_type="tournament",
        K_tournament=2,
        gene_type=int,
        gene_space=list(range(n)),
        allow_duplicate_genes=False,
        keep_parents=-1,
        keep_elitism=2
    )

    inicio = time.time()
    ga_instance.run()
    fim = time.time()

    melhor_solucao, _, _ = ga_instance.best_solution()
    melhor_rota = [pontos_usados[int(i)] for i in melhor_solucao]
    melhor_custo = custoCaminhoFlyfood(melhor_rota, distancias_flyfood, ponto_inicio)
    return melhor_rota, melhor_custo, fim - inicio, pop_size * generations


if __name__ == "__main__":
    print("Executando Força Bruta...")
    rota_fb, custo_fb, tempo_fb, av_fb = forca_bruta_flyfood()

    print("Executando Algoritmo Genético...")
    rota_ag, custo_ag, tempo_ag, av_ag = executar_ag_flyfood()

    print("\n" + "="*65)
    print("        RESULTADO COMPARATIVO: FORÇA BRUTA vs. ALGORITMO GENÉTICO")
    print("="*65)
    print(f"{'Métrica':<25} | {'Força Bruta':<18} | {'Algoritmo Genético':<18}")
    print("-" * 65)
    print(f"{'Menor Custo Obtido':<25} | {custo_fb:<18.2f} | {custo_ag:<18.2f}")
    print(f"{'Tempo de Execução (s)':<25} | {tempo_fb:<18.4f} | {tempo_ag:<18.4f}")
    print(f"{'Rotas Avaliadas':<25} | {av_fb:<18} | {av_ag:<18}")
    print("="*65)
    print(f"Rota Perfeita (FB) : R -> {' -> '.join(rota_fb)} -> R")
    print(f"Rota Obtida (AG)   : R -> {' -> '.join(rota_ag)} -> R")
    print("="*65)