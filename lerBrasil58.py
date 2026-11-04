from pathlib import Path
import random

QTDE_CIDADES = 58

def ler_distancias(caminho_arquivo: Path, qtde_cidades: int = QTDE_CIDADES):
    """Lê os pesos da parte triangular superior de uma instância TSP."""
    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    with caminho_arquivo.open(encoding="utf-8") as arquivo:
        pesos = [int(token) for token in arquivo.read().split()]

    quantidade_esperada = qtde_cidades * (qtde_cidades - 1) // 2
    if len(pesos) != quantidade_esperada:
        raise ValueError(
            f"Arquivo TSP inválido: esperados {quantidade_esperada} pesos, "
            f"mas foram encontrados {len(pesos)}."
        )

    distancias = {}
    indice = 0
    for i in range(1, qtde_cidades):
        for j in range(i + 1, qtde_cidades + 1):
            peso = pesos[indice]
            indice += 1
            distancias[(i, j)] = peso
            distancias[(j, i)] = peso

    for i in range(1, qtde_cidades + 1):
        distancias[(i, i)] = 0

    return distancias

diretorio_script = Path(__file__).parent
caminho_arquivo = diretorio_script / "edgesbrasil58.tsp"
distancias = ler_distancias(caminho_arquivo)

def custoCaminho(permutacao, dicDistancias):
    """Calcula o custo total de um circuito fechado (retornando à cidade de origem)."""
    n = len(permutacao)
    if n < 2:
        raise ValueError("A rota deve conter pelo menos duas cidades.")

    soma = 0
    for i in range(n):
        a = int(permutacao[i])
        b = int(permutacao[(i + 1) % n])  # Fecha o ciclo no último elemento
        
        try:
            soma += dicDistancias[(a, b)]
        except KeyError as erro:
            raise ValueError(f"A aresta ({a}, {b}) não existe no dicionário.") from erro

    return soma

def inicializaPopulacao(tamanho, qtdeCidades):
    """Gera uma população inicial com permutações de 1 até qtdeCidades."""
    populacao = []
    base_cidades = list(range(1, qtdeCidades + 1))
    for _ in range(tamanho):
        individuo = base_cidades.copy()
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao

def calculaAptidao(populacao, dicDistancias):
    """Retorna uma lista de custos para a população fornecida."""
    return [custoCaminho(elem, dicDistancias) for elem in populacao]