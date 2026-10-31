from pathlib import Path
import random


NOME_ARQUIVO_PADRAO = "matriz.txt"
PONTO_INICIO_PADRAO = "R"


def carregar_matriz_flyfood(
    caminho_arquivo: Path | str = NOME_ARQUIVO_PADRAO,
    ponto_inicio: str = PONTO_INICIO_PADRAO,
):
    """Lê uma matriz FlyFood e calcula as distâncias de Manhattan.

    A leitura aceita os dois formatos usados nas instâncias do projeto:
    com a primeira linha contendo ``linhas colunas`` ou sem esse cabeçalho.
    Células com ``0`` representam espaços vazios; qualquer outro valor é
    considerado um ponto identificado por seu rótulo.
    """
    caminho = Path(caminho_arquivo)
    if not caminho.is_absolute():
        caminho = Path(__file__).parent / caminho

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    with caminho.open(encoding="utf-8") as arquivo:
        linhas = [linha.split() for linha in arquivo if linha.strip()]

    if not linhas:
        raise ValueError(f"Arquivo FlyFood vazio: {caminho}")

    dimensoes = _ler_dimensoes(linhas[0])
    if dimensoes is not None:
        quantidade_linhas, quantidade_colunas = dimensoes
        matriz = linhas[1:]
        if len(matriz) != quantidade_linhas:
            raise ValueError(
                f"Matriz inválida: esperadas {quantidade_linhas} linhas, "
                f"mas foram encontradas {len(matriz)}."
            )
    else:
        matriz = linhas
        quantidade_linhas = len(matriz)
        quantidade_colunas = len(matriz[0])

    if quantidade_linhas == 0 or quantidade_colunas == 0:
        raise ValueError("A matriz deve possuir pelo menos uma linha e uma coluna.")

    if any(len(linha) != quantidade_colunas for linha in matriz):
        raise ValueError("Matriz inválida: todas as linhas devem ter o mesmo tamanho.")

    pontos = {}
    for linha, valores in enumerate(matriz):
        for coluna, valor in enumerate(valores):
            if valor != "0":
                if valor in pontos:
                    raise ValueError(f"Ponto duplicado na matriz: {valor}")
                pontos[valor] = (linha, coluna)

    if ponto_inicio not in pontos:
        raise ValueError(f"Ponto de início não encontrado na matriz: {ponto_inicio}")

    distancias = {}
    for ponto_1, (linha_1, coluna_1) in pontos.items():
        for ponto_2, (linha_2, coluna_2) in pontos.items():
            if ponto_1 != ponto_2:
                distancias[(ponto_1, ponto_2)] = (
                    abs(linha_1 - linha_2) + abs(coluna_1 - coluna_2)
                )

    pontos_entrega = [
        ponto for ponto in pontos if ponto != ponto_inicio
    ]
    return distancias, pontos_entrega, ponto_inicio


def _ler_dimensoes(primeira_linha):
    """Retorna as dimensões quando a primeira linha for um cabeçalho válido."""
    if len(primeira_linha) != 2:
        return None

    try:
        dimensoes = tuple(int(valor) for valor in primeira_linha)
    except ValueError:
        return None

    if any(valor <= 0 for valor in dimensoes):
        raise ValueError("As dimensões da matriz devem ser positivas.")
    return dimensoes


def custoCaminhoFlyfood(rota, dic_distancias, ponto_inicio=PONTO_INICIO_PADRAO):
    """Calcula o custo de uma rota fechada, saindo e retornando ao início."""
    rota_completa = [ponto_inicio] + list(rota) + [ponto_inicio]
    custo = 0
    for ponto_atual, proximo_ponto in zip(rota_completa, rota_completa[1:]):
        try:
            custo += dic_distancias[(ponto_atual, proximo_ponto)]
        except KeyError as erro:
            raise ValueError(
                f"A aresta ({ponto_atual}, {proximo_ponto}) não existe."
            ) from erro
    return custo


def inicializaPopulacaoFlyfood(tamanho_pop, lista_pontos):
    """Gera uma população inicial com permutações dos pontos de entrega."""
    populacao = []
    for _ in range(tamanho_pop):
        individuo = list(lista_pontos)
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao


diretorio_script = Path(__file__).parent
caminho_arquivo = diretorio_script / NOME_ARQUIVO_PADRAO
distancias_flyfood, pontos_entrega, ponto_inicio = carregar_matriz_flyfood(
    caminho_arquivo
)
